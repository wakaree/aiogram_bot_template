import { Context } from "grammy";
import type { User } from "@grammyjs/types";
import { sendMessage } from "../helpers/messages";

export const start = async (ctx: Context) => {
  const user: User | undefined = ctx.from;
  console.log(user);
  if (!ctx.chat?.id) return;
  await sendMessage(ctx.chat.id.toString(), "hello", [
    ["« 1", "first"],
    ["‹ 3", "prev"],
  ]);
};
