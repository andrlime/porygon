(* file name -> file content -> Omd.doc (a MD document struct) *)
let generate_md_ast (file_name : string) =
  Io.read_file file_name |> Io.parse_markdown

(* Omd.doc -> Omd.block list *)
let generate_block_list (omd_document : Omd.doc) : 'a Omd.block list =
  List.fold_right
    (fun this_block all_blocks -> this_block :: all_blocks)
    omd_document []
