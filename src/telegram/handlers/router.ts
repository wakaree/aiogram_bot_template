import { Composer } from "grammy";
import { commandConfigHandler } from "./command-config-handler";

export const router = new Composer();

commandConfigHandler.forEach((elem) =>
  router.command(elem.path, (ctx) => elem.handler(ctx)),
);
