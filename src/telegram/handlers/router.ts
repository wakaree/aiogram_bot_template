import { Composer } from "grammy";
import { commandConfigHandler } from "./command-handler";
import { buttonConfigHandler } from "./button-handler";

export const router = new Composer();

commandConfigHandler.forEach((elem) =>
  router.command(elem.path, (ctx) => elem.handler(ctx)),
);

buttonConfigHandler.forEach((elem) =>
  router.callbackQuery(elem.path, async (ctx) => await elem.handler(ctx)),
);
