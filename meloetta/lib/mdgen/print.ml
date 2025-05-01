open Flatten_inline

(** Either a list of blocks or a single block *)
type 'a block_input =
  | BlockList of 'a block_input list
  | SingleBlock of 'a Omd.block

(** [print_block_list (doc : block_input)] Prints an entire markdown AST *)
let rec print_block_list (block_list : 'a Omd.block list) =
  List.iter print_markdown_block block_list

and print_block_list_list (block_list_list : 'a Omd.block list list) =
  List.iter print_block_list block_list_list

(** [print_markdown_block (block : 'a Omd.block)] Prints a block markdown element *)
and print_markdown_block : 'a Omd.block -> unit = function
  | Omd.Paragraph (_, paragraph) -> print_paragraph paragraph
  | Omd.List (_, list_type, list_spacing, list) -> print_list list_type list_spacing list
  | Omd.Blockquote (_, blocks) -> print_blockquote blocks
  | Omd.Thematic_break _ -> Printf.printf "something else\n"
  | Omd.Heading (_, heading_level, heading_content) ->
    print_heading heading_level heading_content
  | Omd.Code_block (_, lang, content) -> print_code_block lang content
  | Omd.Html_block (_, html) -> print_html_block html
  | Omd.Definition_list (_, definitions) -> print_definition_list definitions
  | Omd.Table (_, header_rows, rows) -> print_table header_rows rows

(** [print_paragraph (paragraph: 'a Omd.inline)] Prints a paragraph Omd.block AST node *)
and print_paragraph (paragraph : 'a Omd.inline) =
  Printf.printf "[paragraph] %s" (flatten paragraph)

(** [print_list (list_type : Omd.list_type) (list_spacing : Omd.list_spacing)] Prints a List Omd.block AST node *)
and print_list
      (list_type : Omd.list_type)
      (list_spacing : Omd.list_spacing)
      (blocks : 'a Omd.block list list)
  =
  let list_type_string =
    match list_type with
    | Ordered (_, symbol) -> "ordered:" ^ String.make 1 symbol
    | Bullet symbol -> "bullet:" ^ String.make 1 symbol
  in
  let list_spacing_string =
    match list_spacing with
    | Loose -> "loose"
    | Tight -> "tight"
  in
  Printf.printf "[list:%s:%s]\n" list_type_string list_spacing_string;
  print_block_list_list blocks

(** [print_blockquote (blocks: 'a block list)] Prints a Blockquote Omd.block AST node *)
and print_blockquote (blocks : 'a Omd.block list) = print_block_list blocks

(** [print_thematic_break ()] Prints a Thematic_break Omd.block AST node *)
and print_thematic_break () = print_string "\n\n"

(** [print_heading (level: int) (inline: 'a Omd.inline)] Prints a Heading Omd.block AST node *)
and print_heading (level : int) (inline : 'a Omd.inline) =
  Printf.printf "[H%d] %s" level (flatten inline)

(** [print_code_block (lang: string) (code: string)] Prints a Code_block Omd.block AST node *)
and print_code_block (lang : string) (code : string) =
  Printf.printf "[code:%s] %s" lang code

(** [print_html_block (html: string)] Prints a Html_block Omd.block AST node *)
and print_html_block (html : string) = Printf.printf "[html] %s" html

(** [print_definition_list] Prints a Definition_list Omd.block AST node, NOT IMPLEMENTED *)
and print_definition_list _ = failwith "Definitions list are not implemented"

(** [print_table] Prints a Table Omd.block AST node, NOT IMPLEMENTED *)
and print_table _ _ = failwith "Tables are not implemented"
