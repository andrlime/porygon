open Omd

(* DEBUG: Flattens an omd node into text *)
let rec flatten_text (inlines : 'a Omd.inline list) : string =
  inlines
  |> List.map (function
       | Text (_, s) -> s
       | Code (_, s) -> "`" ^ s ^ "`"
       | Emph (_, inner) -> "*" ^ flatten_text [ inner ] ^ "*"
       | Strong (_, inner) -> "**" ^ flatten_text [ inner ] ^ "**"
       | Concat (_, list) -> flatten_text list
       | Hard_break _ | Soft_break _ -> "\n"
       | Link (_, link) -> flatten_text [ link.label ]
       | Image (_, link) -> flatten_text [ link.label ]
       | Html (_, s) -> s)
  |> String.concat ""

(* DEBUG: prints a list of Omd.block *)
let rec display_omd_block_list (blocks : 'a Omd.block list) =
  List.iteri
    (fun i block ->
      match block with
      | Paragraph (_, inlines) ->
          Printf.printf "[%d] Paragraph: %s\n" i (flatten_text [ inlines ])
      | Heading (_, level, inlines) ->
          Printf.printf "[%d] Heading %d: %s\n" i level
            (flatten_text [ inlines ])
      | Code_block (_, lang, body) ->
          Printf.printf "[%d] Code (%s):\n%s\n" i lang body
      | Blockquote (_, blocks) ->
          Printf.printf "[%d] Blockquote:\n" i;
          display_omd_block_list blocks
      | _ -> Printf.printf "[%d] Unknown or unhandled block\n" i)
    blocks
