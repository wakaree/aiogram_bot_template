exports.up = (pgm) => {
  pgm.addColumn("tasks", {
    disposable: {
      type: "boolean",
      notNull: true,
      default: false,
    },
  });
};

exports.down = (pgm) => {
  pgm.dropColumn("tasks", "disposable");
};
