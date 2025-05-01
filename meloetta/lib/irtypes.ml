type heading_level = H1 | H2 | H3 | H4 | H5 | H6
type image_alt = string
type image_src = string
type url_label = string
type url_link = string
type text_t = string
type path_t = string
type props_key_t = string
type props_value_t = string
type llm_prompt_t = string

type inline =
  | Text of text_t
  | Code of text_t (*inline code like `example = 4`*)
  | Italics of inline list
  | Bold of inline list
  | Link of url_link * url_label
  | Image of image_src * image_alt
  | LineBreak
  | InlineList of inline list

type block =
  | InlineElement of inline
  | Paragraph of inline list
  | Heading of heading_level * inline list
  | Code of text_t * text_t (* lang != "llm", content *)
  | Component of {
      (* react component path, props (list of key->value pairs), children *)
      component_path : path_t;
      props : (props_key_t * props_value_t) list;
      children : block list;
    }
  | LLMCall of { model : text_t; prompt : llm_prompt_t; format : string option }
