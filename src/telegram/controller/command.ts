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
  try {
    const createTask = await ctx.conversation.enter("createTaskConversation");
    console.log("adf");
    console.log(createTask);
  } catch (err) {
    console.error("❌ Error in startCreateTaskController:", err);
  }
};
