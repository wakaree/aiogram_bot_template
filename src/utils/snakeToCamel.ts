export const snakeToCamel = <T extends Record<string, any>>(
  obj: Record<string, any>,
): T => {
  const newObj: Record<string, unknown> = {};

  for (const key in obj) {
    if (!Object.prototype.hasOwnProperty.call(obj, key)) continue;

    const camelKey = key.replace(/_([a-z])/g, (_, letter) =>
      letter.toUpperCase(),
    );
    const value = obj[key];
    if (
      value &&
      typeof value === "object" &&
      !Array.isArray(value) &&
      Object.getPrototypeOf(value) === Object.prototype
    ) {
      newObj[camelKey] = snakeToCamel(value);
    } else {
      newObj[camelKey] = value;
    }
  }

  return newObj as T;
};
