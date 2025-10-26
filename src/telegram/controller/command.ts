import { Context } from "grammy";
import { sendMessage } from "../helpers/messages";

export const start = async (ctx: Context) => {
  if (!ctx.chat?.id) return;
  await sendMessage(ctx.chat.id.toString(), "hello", [
    ["« 1", "first"],
    ["‹ 3", "prev"],
  ]);
};
