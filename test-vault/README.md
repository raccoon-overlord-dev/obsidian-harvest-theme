# Harvest test vault

A vault for checking the theme by hand. Only this README is committed; the notes and `.obsidian/` are gitignored. Recreate them from the list below if needed.

## Contents

- 8 top-level folders (Archive, Inbox, Journal, Projects, Reading, Recipes, Templates, Zettel).
- `Projects/Aurora/Deep/Deeper/` nests 4 levels, for indent guides and open / closed folder icons.
- `Welcome.md` and `Scratch.md` are root files.
- `Journal/Autumn walk.md`: the note from the design screenshots (H1–H4, link, tag, bullets, inline code, a Note callout, a comment, `hr`, code).
- `Inbox/Markdown elements.md`: headings H1–H6, links (resolved, unresolved, external), tags, inline code, `%% comments %%`, highlights, tasks, nested lists, blockquote, `hr`, table, footnote.
- `Inbox/Callouts.md`: every callout type, plus collapsed and nested callouts.
- `Inbox/Code blocks.md`: JS, Python, CSS, HTML, Bash, JSON, Rust and a long line.

## Load the theme

From the repository root, build the theme, then link it into the vault:

```sh
python3 build.py
mkdir -p test-vault/.obsidian/themes/Harvest
ln -sfn ../../../../theme.css     test-vault/.obsidian/themes/Harvest/theme.css
ln -sfn ../../../../manifest.json test-vault/.obsidian/themes/Harvest/manifest.json
```

Open `test-vault` as a vault in Obsidian and choose **Settings → Appearance → Themes → Harvest**. After each rebuild, reload the theme by switching to another theme and back, or by restarting Obsidian.

If symlinks don't work on your system (e.g. Windows without developer mode), copy the two files instead.

## What to check

- Dark and light, in Reading view, Live Preview and Source mode: every element in the notes above.
- Seasonal decor: **Leaves**, **Halloween** and **Off**, with the Style Settings plugin installed. Without the plugin you get Leaves. Halloween also switches to the violet-plum palette.
- Leaves: maple before H2, alternating maple bullets, the leaf cluster on `hr`, the oak on Note callouts, the leaf pile at the bottom of the file explorer, leaves in the top-right corner of the note.
- Halloween: pumpkin before H2, skull bullets, bat · pumpkin · bat on `hr`, the ghost on Note callouts, cobwebs, pumpkins, a ghost and bats in the explorer and the note corner.
- Off: a small rotated square before H2, plain bullets and `hr`, no decor.
- Live Preview: put the cursor at the very start of an H2 line; it should sit after the marker. Check that a `%% comment %%` shows as one dashed box.
- File explorer: folders bold with two-tone icons (open / closed), files with page icons, the open file's icon in the accent color, indent guides.
- Renaming: create a folder and a file, clear the name while renaming, and type. The cursor should stay after the icon.
- Heading font: in Style Settings, type another installed font into **Heading font**; H1–H3 should switch.
- Accent color: in **Settings → Appearance → Accent color**, pick a dark color and then a light one. Buttons follow the accent with readable text; headings, links, folders and decor keep their colors.
- Mobile: on a phone or tablet, or on desktop with `app.emulateMobile(true)` in the developer console (`app.emulateMobile(false)` to go back). Tree rows should be about 44px tall with 16px text, headings smaller, code blocks should scroll sideways in Reading view, and on phones there's no decor in the note corner.
