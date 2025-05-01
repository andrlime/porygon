(** [parse_single_file (filename : string)] Wrapped entire compilation process for a single filename *)
let parse_single_file (filename : string) : unit =
  Io.Read_files.read_file @@ filename
  |> Mdgen.Parse.parse_markdown
  |> Mdgen.Print.print_block_list
;;

let () =
  let _ = "./sample_data" |> Io.Read_files.get_md_files |> List.map parse_single_file in
  Printf.printf "Done\n"
;;
