# Load all locales from .env
CURRENT_LOCALES=$(grep '^TELEGRAM_LOCALES=' ./.env | cut -d '=' -f 2)

# Initialize empty variable for processed locales
PROCESSED_LOCALES=""

# Set separator for splitting locales by comma
IFS=','

# Loop through each locale in CURRENT_LOCALES
for lang in $CURRENT_LOCALES; do
    # Append each locale to PROCESSED_LOCALES with a space separator
    PROCESSED_LOCALES="$PROCESSED_LOCALES -l $lang"
done

# Reset IFS to default
unset IFS

# Delete first character (space)
PROCESSED_LOCALES="${PROCESSED_LOCALES#?}"

# Run the script with processed locales as arguments
# shellcheck disable=SC2086
uv run ftl-extract \
    app assets/messages \
    --default-ftl-file messages.ftl $PROCESSED_LOCALES
