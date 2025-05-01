(** [format_inline_string (label : string) (inner_body : string)] Formats a single inline string into a loggable format *)
let format_inline_string (label : string) (inner_body : string) =
  "[" ^ label ^ "]" ^ " " ^ inner_body ^ "\n"
;;

(** [flatten_inline_list (inlines : 'a Omd.inline list)] Flatten a list of Omd.inline elements *)
let rec flatten_inline_list (inlines : 'a Omd.inline list) =
  inlines |> List.map flatten |> String.concat ""

(** [flatten (_ : Omd.inline)] Dispatches the correct flatten function for Omd.inline *)
and flatten : 'a Omd.inline -> string = function
  | Omd.Concat (_, inlines) -> format_inline_string "concat" (flatten_concat inlines)
  | Omd.Text (_, text) -> format_inline_string "text" (flatten_text text)
  | Omd.Emph (_, inline) -> format_inline_string "emph" (flatten_emph inline)
  | Omd.Strong (_, inline) -> format_inline_string "strong" (flatten_strong inline)
  | Omd.Code (_, code) -> format_inline_string "code_inline" (flatten_code code)
  | Omd.Hard_break _ -> format_inline_string "hard_break" (flatten_hard_break ())
  | Omd.Soft_break _ -> format_inline_string "soft break" (flatten_soft_break ())
  | Omd.Link (_, link) -> format_inline_string "link" (flatten_link link)
  | Omd.Image (_, link) -> format_inline_string "image" (flatten_link link)
  | Omd.Html (_, html) -> format_inline_string "html" (flatten_html html)

(** [flatten_concat (inlines : 'a Omd.inline list)] Flattens a concat inline element *)
and flatten_concat (inlines : 'a Omd.inline list) : string = flatten_inline_list inlines

(** [flatten_text (text : string)] Converts a Text inline to string *)
and flatten_text (text : string) : string = text

(** [flatten_emph (inline : 'a Omd.inline)] Converts an Emph inline to string *)
and flatten_emph (inline : 'a Omd.inline) : string = flatten inline

(** [flatten_strong (inline : 'a Omd.inline)] Converts a Strong inline to string *)
and flatten_strong (inline : 'a Omd.inline) : string = flatten inline

(** [flatten_code (code : string)] Converts a Code inline to string *)
and flatten_code (code : string) : string = code

(** [flatten_hard_break] Converts a Hard_break inline to string *)
and flatten_hard_break () : string = "\n\n"

(** [flatten_soft_break] Converts a Soft_break inline to string *)
and flatten_soft_break () : string = "\n"

(** [flatten_link (link : 'a Omd.link)] Converts a Link inline to string *)
and flatten_link (link : 'a Omd.link) : string = flatten link.label

(** [flatten_image (link : 'a Omd.link)] Converts an Image inline to string *)
and flatten_image (link : 'a Omd.link) : string = flatten link.label

(** [flatten_html (html : string)] Converts an Html inline to string *)
and flatten_html (html : string) : string = html
