(** [parse_markdown (raw_markdown : string)] Takes a raw markdown string and parses it using Omd into an unannotated Markdown AST *)
let parse_markdown (raw_markdown : string) : 'a Omd.block list =
  Omd.of_string raw_markdown
;;
