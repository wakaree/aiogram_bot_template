import { Day } from "../../enums/day.enum";
import { i18n } from "../bot";
import { DayKeyboardEnum } from "../enum/day-keyboard.enum";
import { editMessage, sendReply } from "../helpers/messages";
import { dayChooseKeyboard } from "../key-board/create-task-keyboard";
import { ScheduledTimeConversation } from "../model/sheduled-time-conversation";
import { BotContext } from "../type/context";
import { MyConversation } from "../type/conversation";

export const scheduledTime = async (
  conversation: MyConversation,
  ctx: BotContext,
  idMessage: number,
): Promise<ScheduledTimeConversation> => {
  if (!ctx?.chat?.id) throw Error;
  const locale = await conversation.external(
    () => ctx.session?.__language_code || "en",
  );

  const dayButton = await dayChooseKeyboard((name: string) =>
    i18n.t(locale, name),
  );
  const text = i18n.t(locale, "chooseDay") + " ";
  await editMessage(ctx.chat.id, idMessage, text, dayButton);
  const actionChooseDay = await conversation.waitFor("callback_query:data");
  const choiceChooseDay = actionChooseDay.callbackQuery.data;
  const selectedDay: Day = Object.entries(DayKeyboardEnum).find(
    ([, v]) => v === choiceChooseDay,
  )?.[0] as Day;
  await editMessage(
    ctx.chat.id,
    idMessage,
    i18n.t(locale, "chooseTime", { day: selectedDay }),
  );
  //validation
  const msgTime = await conversation.waitFor("message:text");
  const time = msgTime.message.text;

  return {
    day: selectedDay,
    timeSlots: time,
  };
};
