export const regularChooseKeyboard = async (
  CtxT: (name: string) => string,
): Promise<string[][]> => {
  return [
    [CtxT("regularButtonChooseAction"), "regularButtonChooseAction"],
    [CtxT("oneTimeButtonChooseAction"), "oneTimeButtonChooseAction"],
  ];
};
export const dayChooseKeyboard = async (
  CtxT: (name: string) => string,
): Promise<string[][]> => {
  return [
    [
      CtxT("createTaskMondayButtonChooseAction"),
      "createTaskMondayButtonChooseAction",
    ],
    [
      CtxT("createTaskTuesdayButtonChooseAction"),
      "createTaskTuesdayButtonChooseAction",
    ],
    [
      CtxT("createTaskWednesdayButtonChooseAction"),
      "createTaskWednesdayButtonChooseAction",
    ],
    [
      CtxT("createTaskThursdayButtonChooseAction"),
      "createTaskThursdayButtonChooseAction",
    ],
    [
      CtxT("createTaskFridayButtonChooseAction"),
      "createTaskFridayButtonChooseAction",
    ],
    [
      CtxT("createTaskSaturdayButtonChooseAction"),
      "createTaskSaturdayButtonChooseAction",
    ],
    [
      CtxT("createTaskSundayButtonChooseAction"),
      "createTaskSundayButtonChooseAction",
    ],
  ];
};
export const dayAddKeyboard = async (
  CtxT: (name: string) => string,
): Promise<string[][]> => {
  const buttonChooseAction = await dayChooseKeyboard(CtxT);
  return [[CtxT("createTaskTime"), "createTaskTime"], ...buttonChooseAction];
};
