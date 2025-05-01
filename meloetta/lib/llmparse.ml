open Irtypes

let generate_prompt (prompt : string) (format : string option) =
  let system_prompt =
    "You are a text-based Markdown game engine language model. Below is a \
     prompt for you to respond to. You must respond exactly in the format it \
     specifies. You MUST not include any extraneous information including \
     reasoning."
  in

  let response_format =
    match format with
    | Some "bulleted" ->
        "You must respond using Markdown bullet points, i.e. - content\n\
         - more content."
    | _ -> invalid_arg "unsupported feature"
  in

  system_prompt ^ "\n\n" ^ prompt ^ "\n\n" ^ response_format

let get_llm_body_tags (body : string) : (string, string) Hashtbl.t =
  let tag_table = Hashtbl.create 4 in

  body |> String.split_on_char '\n'
  |> List.iter (fun line ->
         let line = String.trim line in
         if String.starts_with ~prefix:"@" line then
           match String.index_opt line ' ' with
           | Some i ->
               let key = String.sub line 1 (i - 1) in
               let value =
                 String.sub line (i + 1) (String.length line - i - 1)
                 |> String.trim
               in
               Hashtbl.add tag_table key value
           | None -> ());

  tag_table

(* Take the body of an LLM request and parse it for the AST *)
(*

Format of the inside of a code block
@model gpt-4.1
@prompt "quoted prompt goes here"
@format "bulleted" (or something else, for later support)

*)
let parse_llm_body (body : string) =
  Printf.printf "*** parsing LLM body ***\n";
  let keys = get_llm_body_tags body in
  Io.print_map keys;

  LLMCall
    {
      model = Hashtbl.find keys "model";
      prompt = Hashtbl.find keys "prompt";
      format = Hashtbl.find_opt keys "format";
    }
