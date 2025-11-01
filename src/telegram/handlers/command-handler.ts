import { start } from "../controller/command";

export const commandConfigHandler: ConfigCommandHandlers[] = [
  {
    path: "start",
    handler: start,
  },
];

export interface ConfigCommandHandlers {
  path: string;
  handler: Function;
}
