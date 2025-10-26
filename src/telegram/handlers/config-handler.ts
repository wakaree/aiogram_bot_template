import { FilterQuery } from "grammy";
import { start } from "repl";

// export const configPath: ConfigHandlers[] = [
//   {
//     path: "message:text",
//     handler: start,
//   },
// ];
export interface ConfigHandlers {
  path: FilterQuery;
  handler: Function;
}
