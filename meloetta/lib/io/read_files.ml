(** [get_md_files (folder : string)] Recursively returns all markdown files in a folder *)
let rec get_md_files (folder : string) : string list =
  Sys.readdir folder
  |> Array.to_list
  |> List.fold_left
       (fun all_entries entry ->
          let file_path = Filename.concat folder entry in
          if Sys.is_directory file_path
          then get_md_files file_path @ all_entries
          else if Filename.check_suffix entry ".md"
          then file_path :: all_entries
          else all_entries)
       []
;;

(** [read_file (file_name : string)] Reads and returns the raw content of a non-encoded file *)
let read_file (file_name : string) : string =
  In_channel.with_open_text file_name In_channel.input_all
;;
