# Ren'Py MCP Reference

This project uses the local Ren'Py MCP server at:

`C:\Users\blank\Documents\RenPy_Projects\Tractir\renpy_mcp_server`

Current environment expected by the server:

- `RENPY_MCP_WORKSPACE=C:\Users\blank\Documents\RenPy_Projects\Tractir`
- `RENPY_SDK_PATH=C:\Users\blank\renpy\renpy-8.5.2-sdk`

The MCP server is useful for project inspection, generated assets, builds, and web preview. It must not replace the Tractir code model: room classes, object menus, NPC classes, and event/thread logic remain the source of truth. For normal source edits in Tractir, prefer surgical `.rpy` patches and direct Ren'Py labels over wrapper or dispatcher code.

## Tools

| Tool | Purpose | Our Use |
| --- | --- | --- |
| `list_projects` | Lists projects visible under the MCP workspace root. | Confirm the server sees the correct workspace and project names after path/env changes. |
| `list_project_files(project_name)` | Lists files under a project's `game` directory with paths, sizes, and suffixes. | Quick inspection of generated/simple projects. For Tractir, use normal repo tools first when exact source tracing is needed. |
| `read_project_file(project_name, file_path)` | Reads one file from a project's `game` directory. | Useful for MCP-client inspection. In our Codex workflow, direct filesystem reads are usually clearer. |
| `edit_project_file(project_name, file_path, content)` | Overwrites or creates one file in a project's `game` directory. | Avoid for Tractir unless explicitly needed. It overwrites whole files, so it is riskier than a surgical patch. |
| `create_project(name, template=None)` | Creates a new Ren'Py project from the server template. | For new prototypes only. Do not use inside Tractir's live game structure. |
| `generate_background(project_name, description, style=None, base_filename=None)` | Generates a visual novel background image using Gemini and saves it as a project asset. | Useful for new backgrounds when image generation is requested. Requires `GEMINI_API_KEY`. |
| `generate_character(project_name, character_name, description, pose=None, emotion=None, style=None, generate_emotions=False)` | Generates a character sprite, optionally with emotion variants, removes background, and normalizes sprite height. | Useful for prototype sprites or new art passes. Requires `GEMINI_API_KEY`; not needed for existing Tractir portraits unless requested. |
| `generate_script(project_name, script_name, script_content)` | Writes a generated `.rpy` script and may update template `script.rpy` to call its label. | Not suitable for Tractir story refactors because it assumes small generated VN scripts. Use direct `.rpy` labels and event/thread classes instead. |
| `build_project(project_name, target="web", force_rebuild=False)` | Runs Ren'Py build/distribution for a target, commonly web. | Use for generated/prototype projects or explicit distribution checks. For Tractir runtime validation, `renpy.exe . compile` or `renpy.exe . lint` is usually the focused check. |
| `start_web_preview(project_name)` | Starts a local HTTP server for an existing web build. | Use only after a web build exists and browser preview is needed. |
| `stop_web_preview(project_name)` | Stops the local preview server for a project. | Clean up preview servers after testing. |

## Resource

| Resource | Purpose | Our Use |
| --- | --- | --- |
| `renpy://build/{project_name}` | Human-readable summary of the latest web build and build log location. | Check whether a web build exists and whether it is ready for preview. |

## Tractir Rules

- Use `C:\Users\blank\Documents\RenPy_Projects\Tractir` as the only active project path.
- Do not use or recreate `C:\Users\blank\Documents\Ren'Py_Projects`.
- Keep `renpy_mcp_server` as a helper, not as the architecture owner.
- Do not use MCP script generation to create wrapper labels, refresh labels, rebuild labels, dispatcher layers, recursive menu loops, or whole-file rewrites in Tractir.
- Use generated image tools only when new assets are actually requested.
- Missing `GEMINI_API_KEY` only disables Gemini image/text provider features; it does not break MCP project/path integrity.
