# Meloetta: LLM Text Based Game Compiler

![image](icon.png)

Text based game engines democratise game creation to the general public. However, codeless platforms like [Twine](https://twinery.org) do not truly support calling APIs and leveraging the story generation capability of large language models. While janky workarounds exist, they do not work well, and React becomes an easier platform to create equivalent text-based games. However, React is not inherently user friendly for non-technical people. This project seeks to address a middle-ground by compiling Markdown files with minimal code that embed API calls and LLM prompts into skeleton React pages and components that can be run using the React runtime. The compilation engine is written in **OCaml** to compile a folder of Markdown and config files into an intermediate representation of building blocks, parsing those building blocks to include API, LLM, and possibly remote procedure calls, and programatically generate stateful React components. A minimal Flask app is created as a backend to host the API calling. Both apps are bundled with Dockerfiles, and the apps are run together using Docker Compose. The project here is not a compiler in the sense that LLVM and related projects are. To compile human language to human language via intermediate ASTs is not the same as generating byte code. However, many principles are shared, and hopefully somebody will find this project interesting.

## Why OCaml?
OCaml has incredible pattern matching that far exceeds using C++ templates and writing boilerplate code. While that would be intellectually stimulating too, using `|>` to pipe input between function calls leads to less annoying boilerplate than seeing `template <typename T>` probably a few hundred times.

## Roadmap
- [ ] Design and Document the IR
- [ ] Folder of files -> list of file names -> list of raw file content -> list of md parsed file content -> list of IR ASTs -> list of React component trees -> React app
- [ ] Make prompts and responses interactive / have callbacks
- [ ] Implement state and backend
- [ ] Implement Docker support
- [ ] Implement 4o image generation support
- [ ] Implement arbitrary callback

## Example
Consider a text-based game to teach people about budgeting:
```md
A man walked into a grocery store with $30. His needs are
food (6/10)
fun (5/10)
health (4/10)

Please select which items to purchase:
::: start llm
::: state -> "money"
::: prompt -> "You are a grocery store with items in the following categories: food, fun, and health. Please provide a list of four items and their prices for an individual to purchase. Some must be more expensive than others. A patron should not be able to buy more than 3 items without exceeding their budget of %budget%."
::: response -> <Choice onClick={() => {...}}>%response%</Choice>
::: end llm
```
and the output might look like the following. It would be also be very cool to enable LLM generated variable values, so the response callback can really be anything.

### Output
A man walked into a grocery store with $30. His needs are
food (6/10)
fun (5/10)
health (4/10)

Please select which items to purchase:
- <button>Tomato (food +2, health +2, fun -3, $6)</button>
- <button>Video Game (food -5, health +1, fun +8, $80)</button>
- <button>Toothpaste (food 0, health +2, fun 0, $4)</button>
- <button>Milk (food +2, health +2, fun 0, $7)</button>

## Conclusion
The goal is to enable prompts like these to generate choices from an LLM prompt to nonlinearise previouisly linear text-based games. There is a lot of room for story telling using the voice of a large language model. While these models do have inherent biases, good prompt engineering can exploit their strengths.
