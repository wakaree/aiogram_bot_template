import { sendMessage } from "../helpers/messages";
import { homeKeyboard } from "../key-board/home-keyboard";
import { UserContext } from "../type/context";

export const start = async (ctx: UserContext) => {
  // const user = ctx.user;
  if (!ctx.chat?.id) return;
  const button = await homeKeyboard(ctx);
  await sendMessage(ctx.chat.id, ctx.t("start"), button);
};

export const startCreateTaskController = async (ctx: UserContext) => {
  await ctx.conversation.enter("createTaskConversation");
};
