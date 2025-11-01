import { startCreateTaskController } from "../controller/command";
import { ConfigCommandHandlers } from "./command-handler";

export const buttonConfigHandler: ConfigCommandHandlers[] = [
  {
    path: "startCreateTask",
    handler: startCreateTaskController,
  },
];
