let print_map map =
  Hashtbl.iter (fun key value -> Printf.printf "%s: %s\n" key value) map

(* Recursively get all md files from a folder *)
let rec get_md_files (folder : string) =
  Sys.readdir folder |> Array.to_list
  |> List.fold_left
       (fun all_entries entry ->
         let file_path = Filename.concat folder entry in
         if Sys.is_directory file_path then get_md_files file_path @ all_entries
         else if Filename.check_suffix entry ".md" then file_path :: all_entries
         else all_entries)
       []

let read_file (file_name : string) =
  In_channel.with_open_text file_name In_channel.input_all

let parse_markdown (raw_markdown : string) = Omd.of_string raw_markdown
