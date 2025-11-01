import { i18n } from "../bot";
import { sendReply } from "../helpers/messages";
import {
  regularChooseKeyboard,
  dayChooseKeyboard,
} from "../key-board/create-task-keyboard";
import { BotContext } from "../type/context";
import { MyConversation } from "../type/conversation";
import { scheduledTime } from "./scheduled-time";

export const createTaskConversation = async (
  conversation: MyConversation,
  ctx: BotContext,
): Promise<void> => {
  const locale = await conversation.external(
    () => ctx.session?.__language_code || "en",
  );

  await ctx.reply(i18n.t(locale, "startCreateTask"));
  const msgTitle = await conversation.waitFor("message:text");
  const title = msgTitle.message.text;
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
  const actionRegular = await conversation.waitFor("callback_query:data");
  const choiceReguular = actionRegular.callbackQuery.data;
  const messageId = actionRegular.callbackQuery.message?.message_id ?? 0;
  await actionRegular.answerCallbackQuery();

  const disposable =
    choiceReguular === "regularButtonChooseAction" ? true : false;
  await scheduledTime(conversation, actionRegular, messageId);
};
