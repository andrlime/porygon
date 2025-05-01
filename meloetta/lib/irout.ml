(* TODO: Support indents *)

let convert_inline_to_jsx (inline : Irtypes.inline) : string =
  let inside =
    match inline with
    | Text _ -> "aaa"
    | Code _ -> "aaa"
    | Italics _ -> "aaa"
    | Bold _ -> "aaa"
    | Link (_, _) -> "aaa"
    | Image (_, _) -> "aaa"
    | LineBreak -> "\n"
    | InlineList _ -> "aaa"
  in

  "<>" ^ inside ^ "</>\n"

let convert_block_to_jsx (block : Irtypes.block) : string =
  let inside =
    match block with
    | InlineElement _ -> "THING"
    | Paragraph _ -> "PARAGRAPH"
    | Heading (_, _) -> "HEADING"
    | Code (_, _) -> "CODE BLOCK"
    | Component _ -> "COMPONENT"
    | LLMCall _ -> "LLM CALL"
  in

  "<>\n" ^ inside ^ "\n</>\n"

let dump_as_jsx (intermediate : Irtypes.block list) : string =
  let inside =
    List.fold_right
      (fun this_block all_blocks ->
        all_blocks ^ convert_block_to_jsx this_block)
      intermediate ""
  in

  "<>\n\n" ^ inside ^ "\n</>\n"
