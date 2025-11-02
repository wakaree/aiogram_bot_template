import { CreateTask } from "../../models/task.model";
import { i18n } from "../bot";
import {
  handlerGetCallbackQueryMessage,
  handlerGetTextMessage,
} from "../helpers/conversation";
import { sendReply } from "../helpers/messages";
import { regularChooseKeyboard } from "../key-board/create-task-keyboard";
import { BotContext } from "../type/context";
import { MyConversation } from "../type/conversation";
import { scheduledTimesConversation } from "./scheduled-time";

export const createTaskConversation = async (
  conversation: MyConversation,
  ctx: BotContext,
): Promise<CreateTask> => {
  const locale = await conversation.external(
    () => ctx.session?.__language_code || "en",
  );
  await sendReply(ctx, i18n.t(locale, "startCreateTask"));
  const { title } = await handlerGetTextMessage(conversation);
  await ctx.reply(i18n.t(locale, "enterDescriptionTaskTitle", { title }), {
    parse_mode: "Markdown",
  });
  const msgDescription = await conversation.waitFor("message:text");
  const description = msgDescription.message.text;
  const regularButton = await regularChooseKeyboard((name: string) =>
    i18n.t(locale, name),
  );
  await sendReply(
    ctx,
    i18n.t(locale, "enterRegularTime", {
      title,
      description,
    }),
    regularButton,
  );
  const { messageId, choice: choiceReguular } =
    await handlerGetCallbackQueryMessage(conversation);

  const disposable =
    choiceReguular === "regularButtonChooseAction" ? true : false;
  const time = await scheduledTimesConversation(conversation, ctx, messageId);
  console.log("✅ reached before return", {
    title,
    description,
    disposable,
    time,
  });
  return {
    title,
    description,
    disposable,
    scheduledTime: time,
  };
};
