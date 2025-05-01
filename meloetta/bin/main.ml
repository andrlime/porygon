open Meloetta

let () =
  let _ =
    Io.get_md_files "sample_data"
    |> List.map (fun file_name ->
           let intermediate =
             Compile.generate_md_ast file_name
             |> Compile.generate_block_list |> Ir.parse_omd_block_list
           in

           Irout.dump_as_jsx intermediate |> Printf.printf "%s")
  in
  Printf.printf "done"

(* |> List.map(fun markdown_content ->
    Filesystem.parse_file_into_blocks markdown_content
  )
  |> List.map(fun markdown_content ->
    Ir.print_omd_block markdown_content
  ) *)
