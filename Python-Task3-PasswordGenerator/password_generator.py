import secrets
import string


AMBIGUOUS_CHARACTERS = "0Ol1I"


def remove_ambiguous_characters(characters):
    """Remove visually confusing characters from a character set."""

    for character in AMBIGUOUS_CHARACTERS:
        characters = characters.replace(character, "")

    return characters


def generate_password(
    length,
    use_uppercase,
    use_lowercase,
    use_numbers,
    use_symbols,
    exclude_ambiguous=False
):
    # Check password length
    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")

    # Store the selected character groups
    character_sets = []

    # Uppercase letters
    if use_uppercase:
        characters = string.ascii_uppercase

        if exclude_ambiguous:
            characters = remove_ambiguous_characters(characters)

        character_sets.append(characters)

    # Lowercase letters
    if use_lowercase:
        characters = string.ascii_lowercase

        if exclude_ambiguous:
            characters = remove_ambiguous_characters(characters)

        character_sets.append(characters)

    # Numbers
    if use_numbers:
        characters = string.digits

        if exclude_ambiguous:
            characters = remove_ambiguous_characters(characters)

        character_sets.append(characters)

    # Symbols
    if use_symbols:
        characters = string.punctuation

        if exclude_ambiguous:
            characters = remove_ambiguous_characters(characters)

        character_sets.append(characters)

    # At least two character types must be selected
    if len(character_sets) < 2:
        raise ValueError(
            "Please select at least two character types."
        )

    # One character from every selected type
    password_characters = []

    for characters in character_sets:
        password_characters.append(
            secrets.choice(characters)
        )

    # Combine all selected character types
    all_characters = "".join(character_sets)

    # Fill the remaining positions
    remaining_characters = length - len(password_characters)

    for _ in range(remaining_characters):
        password_characters.append(
            secrets.choice(all_characters)
        )

    # Shuffle the password
    secrets.SystemRandom().shuffle(password_characters)

    # Convert the list into a string
    return "".join(password_characters)


def calculate_password_strength(
    length,
    use_uppercase,
    use_lowercase,
    use_numbers,
    use_symbols
):
    # Count how many character types are selected
    character_type_count = sum([
        use_uppercase,
        use_lowercase,
        use_numbers,
        use_symbols
    ])

    # Strong password
    if length >= 16 and character_type_count >= 3:
        return "Strong"

    # Medium password
    elif length >= 12 and character_type_count >= 2:
        return "Medium"

    # Weak password
    else:
        return "Weak"


