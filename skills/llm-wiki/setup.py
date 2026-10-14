#!/usr/bin/env python3
"""Bootstrap the LLM wiki structure in a Trilium instance through ETAPI.

Creates (idempotently, found again by label on re-runs):

    LLM Wiki                      #llmWiki
    ├── Schema                    #llmWikiSchema          (content: schema.html)
    ├── Wiki                      #llmWikiPart=wiki
    ├── Sources                   #llmWikiPart=sources  #readOnly(inheritable) #wikiSource(inheritable)
    ├── Templates                 #llmWikiPart=templates
    │   ├── Wiki Topic Hub        #template #wiki #wikiType=hub     + promoted-attribute definitions
    │   ├── Wiki Source Summary   #template #wiki #wikiType=summary + promoted-attribute definitions
    │   ├── Wiki Concept          #template #wiki #wikiType=concept + promoted-attribute definitions
    │   └── Wiki Entity           #template #wiki #wikiType=entity  + promoted-attribute definitions
    └── Views                     #llmWikiPart=views
        └── saved searches (type=search, #searchString=...)

Standard library only. Talks to Trilium's ETAPI directly, not to trilium-mcp,
so it needs network access to Trilium itself.

    ./setup.py --url http://localhost:8080 --token "$TRILIUM_ETAPI_TOKEN"
    ./setup.py --dry-run            # print what would be created
    ./setup.py --parent <noteId>    # place "LLM Wiki" under a note other than root
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------- declarations

# Promoted attribute definitions: (kind, name, definition value)
# label definition syntax: promoted,single|multiple,<text|number|boolean|date|url>
# relation definition syntax: promoted,single|multiple
COMMON_PROMOTED = [
    ("label", "wikiTopic", "promoted,multiple,text"),
    ("label", "wikiStatus", "promoted,single,text"),
    ("label", "aiAssisted", "promoted,single,boolean"),
]

TEMPLATES = [
    {
        "title": "Wiki Topic Hub",
        "wikiType": "hub",
        "icon": "bx bx-sitemap",
        "promoted": [
            ("label", "wikiTopic", "promoted,single,text"),
            ("label", "wikiStatus", "promoted,single,text"),
        ],
        "content": (
            "<h2>Scope</h2><p>What this topic covers and what it deliberately leaves out.</p>"
            "<h2>Key pages</h2><ul><li>Concepts: </li><li>Entities: </li><li>Sources: </li></ul>"
            "<h2>Open questions</h2><ul><li></li></ul>"
        ),
    },
    {
        "title": "Wiki Source Summary",
        "wikiType": "summary",
        "icon": "bx bx-file-find",
        "promoted": COMMON_PROMOTED + [("relation", "wikiSource", "promoted,single")],
        "content": (
            "<h2>Summary</h2><p></p>"
            "<h2>Key claims</h2><ul><li></li></ul>"
            "<h2>Data and quotes</h2><ul><li></li></ul>"
            "<h2>Relevance</h2><p>How this changes or confirms existing pages.</p>"
            "<h2>Open questions</h2><ul><li></li></ul>"
        ),
    },
    {
        "title": "Wiki Concept",
        "wikiType": "concept",
        "icon": "bx bx-bulb",
        "promoted": COMMON_PROMOTED + [("relation", "relatesTo", "promoted,multiple")],
        "content": (
            "<h2>Definition</h2><p></p>"
            "<h2>Evidence</h2><ul><li></li></ul>"
            "<h2>Contradictions</h2><p>None recorded.</p>"
            "<h2>Related</h2><ul><li></li></ul>"
        ),
    },
    {
        "title": "Wiki Entity",
        "wikiType": "entity",
        "icon": "bx bx-id-card",
        "promoted": COMMON_PROMOTED
        + [
            ("label", "entityKind", "promoted,single,text"),
            ("relation", "relatesTo", "promoted,multiple"),
        ],
        "content": (
            "<h2>Who or what</h2><p></p>"
            "<h2>Why it matters here</h2><p></p>"
            "<h2>Mentioned in</h2><ul><li></li></ul>"
        ),
    },
]

# (marker slug, title, search string). Slugs stay alphanumeric: Trilium's search
# parser treats an unquoted hyphenated label value as several tokens. Templates own
# #wiki/#wikiType themselves, so #!template keeps them out of the page views.
VIEWS = [
    ("sourcesPending", "Sources not yet summarised", "#wikiSource #!llmWikiPart note.targetRelationCount = 0"),
    ("stubs", "Stubs", "#wiki #!template #wikiStatus=stub orderBy note.dateModified desc"),
    ("drafts", "Drafts awaiting review", "#wiki #!template #wikiStatus=draft orderBy note.dateModified desc"),
    # The != clause must come first: Trilium (0.106) returns nothing for a != test on an
    # inherited label when another label filter precedes it.
    ("orphans", "Orphan pages", "#wikiType != hub note.targetRelationCountIncludingLinks = 0 #wiki #!template"),
    ("recent", "Recently changed wiki pages", "#wiki #!template orderBy note.dateModified desc limit 50"),
    ("hubs", "Topic hubs", "#wikiType=hub #!template orderBy note.title"),
]

# ---------------------------------------------------------------------- client


class Etapi:
    def __init__(self, base: str, token: str, dry_run: bool = False):
        self.base = base.rstrip("/")
        if not self.base.endswith("/etapi"):
            self.base += "/etapi"
        self.token = token
        self.dry_run = dry_run
        self._fake = 0

    def _call(self, method: str, path: str, body=None, raw: bytes | None = None, ctype=None):
        url = self.base + path
        data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", self.token)
        if data is not None:
            req.add_header("Content-Type", ctype or "application/json")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                text = resp.read().decode()
        except urllib.error.HTTPError as e:
            sys.exit(f"ETAPI {method} {path} -> {e.code}: {e.read().decode()[:300]}")
        return json.loads(text) if text else None

    def get(self, path):
        return self._call("GET", path)

    def search(self, query: str, **params) -> list[dict]:
        q = urllib.parse.urlencode({"search": query, **params})
        return self.get(f"/notes?{q}")["results"]

    def _write(self, method, path, body=None, **kw):
        if self.dry_run:
            print(f"  [dry-run] {method} {path} {json.dumps(body)[:160] if body else ''}")
            self._fake += 1
            return {"note": {"noteId": f"DRY{self._fake}"}, "attributeId": f"DRY{self._fake}"}
        return self._call(method, path, body, **kw)

    def create_note(self, parent: str, title: str, content: str, type_: str = "text", mime=None) -> str:
        body = {"parentNoteId": parent, "title": title, "type": type_, "content": content}
        if mime:
            body["mime"] = mime
        return self._write("POST", "/create-note", body)["note"]["noteId"]

    def add_attr(self, note: str, type_: str, name: str, value: str = "", inheritable=False):
        return self._write(
            "POST",
            "/attributes",
            {"noteId": note, "type": type_, "name": name, "value": value, "isInheritable": inheritable},
        )

    def patch_attr(self, attribute_id: str, value: str):
        return self._write("PATCH", f"/attributes/{attribute_id}", {"value": value})

    def put_content(self, note: str, html: str):
        if self.dry_run:
            print(f"  [dry-run] PUT /notes/{note}/content ({len(html)} chars)")
            return
        self._call("PUT", f"/notes/{note}/content", raw=html.encode(), ctype="text/plain; charset=utf-8")


# ----------------------------------------------------------------------- setup


# Labels a note carries once; a changed declaration updates them in place.
SINGLE_VALUED = {"searchString", "iconClass"}


def own_attrs(note: dict) -> set[tuple[str, str, str]]:
    return {(a["type"], a["name"], a["value"]) for a in note["attributes"] if a["noteId"] == note["noteId"]}


def find_one(api: Etapi, query: str) -> dict | None:
    """Find the single note *owning* the marker label. Template instances inherit the
    template's labels, so a plain search for the marker would also return them."""
    name = query[1:].split("=")[0]
    hits = [n for n in api.search(query, fastSearch="true")
            if any(a["noteId"] == n["noteId"] and a["name"] == name for a in n["attributes"])]
    if len(hits) > 1:
        titles = ", ".join(f'"{h["title"]}" ({h["noteId"]})' for h in hits)
        sys.exit(f"Expected at most one note for {query!r}, found {len(hits)}: {titles}")
    return hits[0] if hits else None


def ensure_note(api: Etapi, parent: str, title: str, marker: tuple[str, str], *, content="", type_="text",
                extra_attrs: list[tuple] = ()) -> tuple[str, bool]:
    """Find a note by its marker label (name, value) or create it. Returns (noteId, created)."""
    name, value = marker
    query = f"#{name}={value}" if value else f"#{name}"
    existing = find_one(api, query)
    if existing:
        print(f"  = {title!r} exists ({existing['noteId']})")
        have = own_attrs(existing)
        for a in extra_attrs:
            type_, aname, avalue, *rest = a
            if (type_, aname, avalue) in have:
                continue
            current = next((x for x in existing["attributes"]
                            if x["noteId"] == existing["noteId"] and x["type"] == type_ and x["name"] == aname), None)
            if current and aname in SINGLE_VALUED:
                api.patch_attr(current["attributeId"], avalue)
                print(f"    ~ updated {type_} {aname}: {current['value']!r} -> {avalue!r}")
            else:
                api.add_attr(existing["noteId"], type_, aname, avalue, *(rest or [False]))
                print(f"    + added missing {type_} {aname}={avalue}")
        return existing["noteId"], False
    note_id = api.create_note(parent, title, content, type_)
    api.add_attr(note_id, "label", name, value)
    for a in extra_attrs:
        type_, aname, avalue, *rest = a
        api.add_attr(note_id, type_, aname, avalue, *(rest or [False]))
    print(f"  + created {title!r} ({note_id})")
    return note_id, True


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--url", default=os.environ.get("TRILIUM_SERVER_URL", "http://localhost:8080"),
                   help="Trilium base URL (ETAPI is appended). Default: $TRILIUM_SERVER_URL or http://localhost:8080")
    p.add_argument("--token", default=os.environ.get("TRILIUM_ETAPI_TOKEN"), help="ETAPI token. Default: $TRILIUM_ETAPI_TOKEN")
    p.add_argument("--parent", default="root", help="noteId to create 'LLM Wiki' under. Default: root")
    p.add_argument("--schema", default=HERE / "schema.html", type=Path, help="HTML file for the Schema note")
    p.add_argument("--update-schema", action="store_true", help="overwrite an existing Schema note's content from --schema")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    if not args.token:
        sys.exit("No ETAPI token: pass --token or set TRILIUM_ETAPI_TOKEN")

    api = Etapi(args.url, args.token, args.dry_run)
    info = api.get("/app-info")
    print(f"Trilium {info['appVersion']} at {api.base}" + ("  (dry run)" if args.dry_run else ""))

    print("Root")
    root, _ = ensure_note(api, args.parent, "LLM Wiki", ("llmWiki", ""),
                          content="<p>An LLM-maintained wiki. Start with <strong>Schema</strong>.</p>",
                          extra_attrs=[("label", "iconClass", "bx bx-brain")])

    print("Parts")
    schema_html = args.schema.read_text(encoding="utf-8")
    schema, created = ensure_note(api, root, "Schema", ("llmWikiSchema", ""), content=schema_html,
                                  extra_attrs=[("label", "llmWikiPart", "schema"), ("label", "iconClass", "bx bx-book-open")])
    if not created and args.update_schema:
        api.put_content(schema, schema_html)
        print("    ~ schema content updated")

    ensure_note(api, root, "Wiki", ("llmWikiPart", "wiki"),
                content="<p>Pages the assistant writes. One child per topic hub.</p>",
                extra_attrs=[("label", "iconClass", "bx bx-network-chart")])
    ensure_note(api, root, "Sources", ("llmWikiPart", "sources"),
                content="<p>Raw material: clips, articles, PDFs. Read-only for the assistant.</p>",
                extra_attrs=[("label", "readOnly", "", True), ("label", "wikiSource", "", True),
                             ("label", "iconClass", "bx bx-archive")])
    templates, _ = ensure_note(api, root, "Templates", ("llmWikiPart", "templates"),
                               content="<p>One template per wiki page type.</p>",
                               extra_attrs=[("label", "iconClass", "bx bx-copy-alt")])
    views, _ = ensure_note(api, root, "Views", ("llmWikiPart", "views"),
                           content="<p>Saved searches that drive ingest and lint.</p>",
                           extra_attrs=[("label", "iconClass", "bx bx-filter-alt")])

    print("Templates")
    for t in TEMPLATES:
        attrs = [
            ("label", "template", ""),
            # Not tree-inheritable: instances get these through template inheritance,
            # and a summary under a hub must not inherit the hub's wikiType.
            ("label", "wiki", ""),
            ("label", "wikiType", t["wikiType"]),
            ("label", "iconClass", t["icon"]),
        ]
        # Promoted definitions are *label* attributes named "label:x" / "relation:x".
        attrs += [("label", f"{kind}:{name}", definition) for kind, name, definition in t["promoted"]]
        ensure_note(api, templates, t["title"], ("llmWikiTemplate", t["wikiType"]), content=t["content"], extra_attrs=attrs)

    print("Views")
    for slug, title, query in VIEWS:
        ensure_note(api, views, title, ("llmWikiView", slug), type_="search",
                    extra_attrs=[("label", "searchString", query)])

    print("Done." if not args.dry_run else "Dry run complete; nothing written.")


if __name__ == "__main__":
    main()
