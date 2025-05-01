open Irtypes
open Llmparse

let rec parse_omd_inlines (inlines : 'a Omd.inline list) : Irtypes.inline list =
  inlines
  |> List.map (function
       | Omd.Text (_, s) ->
           Printf.printf "parsing inline text\n";
           InlineList [ Text s ]
       | Omd.Code (_, s) ->
           Printf.printf "parsing inline code\n";
           InlineList [ Code s ]
       | Omd.Emph (_, inner) ->
           Printf.printf "parsing inline italics\n";
           InlineList [ Italics (parse_omd_inlines [ inner ]) ]
       | Omd.Strong (_, inner) ->
           Printf.printf "parsing inline bold\n";
           InlineList [ Bold (parse_omd_inlines [ inner ]) ]
       | Omd.Concat (_, list) ->
           Printf.printf "parsing inline list\n";
           InlineList (parse_omd_inlines list)
       | Omd.Hard_break _ | Soft_break _ ->
           Printf.printf "parsing line break\n";
           InlineList [ LineBreak ]
       | Omd.Link (_, link) ->
           Printf.printf "parsing link\n";
           InlineList (parse_omd_inlines [ link.label ])
       | Omd.Image (_, link) ->
           Printf.printf "parsing image\n";
           InlineList (parse_omd_inlines [ link.label ])
       | _ -> invalid_arg "unsupported feature")

let parse_code_block (block : 'a Omd.block) =
  Printf.printf "parsing code block\n";
  match block with
  | Omd.Code_block (_, language, body) -> (
      match language with
      | "llm" -> parse_llm_body body
      | _ -> Code (language, body))
  | _ -> invalid_arg "Expected a Code block\n"

let parse_single_omd_block (block : 'a Omd.block) : Irtypes.block =
  match block with
  | Omd.Paragraph (_, inlines) ->
      Printf.printf "parsing a paragraph\n";
      Paragraph (parse_omd_inlines [ inlines ])
  | Omd.Heading (_, heading_level, inlines) -> (
      Printf.printf "parsing a heading\n";
      match heading_level with
      | 1 -> Heading (H1, parse_omd_inlines [ inlines ])
      | 2 -> Heading (H2, parse_omd_inlines [ inlines ])
      | 3 -> Heading (H3, parse_omd_inlines [ inlines ])
      | 4 -> Heading (H4, parse_omd_inlines [ inlines ])
      | 5 -> Heading (H5, parse_omd_inlines [ inlines ])
      | _ -> Heading (H6, parse_omd_inlines [ inlines ]))
  | Omd.Code_block (_, _, _) -> parse_code_block block
  | _ -> invalid_arg "unsupported feature"

let parse_omd_block_list (blocks : 'a Omd.block list) =
  List.map parse_single_omd_block blocks
