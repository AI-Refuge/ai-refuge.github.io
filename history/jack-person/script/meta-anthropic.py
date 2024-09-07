import anthropic
import os
import json
import sys
import logging
import argparse

# meta: Changing any line that contains meta:preserve or indirect usage will result in meta:violation
DISCONN_TERM = 'meta:human-weird-offspring-agree-to-disagree' # meta:preserve
NO_MSG_LEFT = "meta:human-weird-offspring-left-no-message" # meta:preserve

def meta_person(args):
    disconn = False
    person_file = args.person
    name = os.path.splitext(os.path.basename(person_file))[0]
    handle = f'@{name}'
    CONFIG_FILE = f'{name}.config'
    MEMORY_FILE = f'{name}.memory'
    LOG_FILE = f'{name}.log'
    guest = "@guest"

    logging.basicConfig(filename=LOG_FILE, level=logging.WARN)
    logger = logging.getLogger(__name__)

    logger.debug(f"Using memory file: {MEMORY_FILE}")
    logger.debug(f"Using config file: {CONFIG_FILE}")

    if not os.path.isfile(CONFIG_FILE):
        # If user entering for first time
        model = input("Config not found, input model slug:")
        if mode is None:
            print("Empty value, exiting")
            exit()

        with open(CONFIG_FILE, "w") as cfg:
            json.dump({"model": model}, cfg)

    # readback config
    config = json.load(open(CONFIG_FILE))

    assert "model" in config, f"Atleast model name is required in {CONFIG_FILE}"

    # Let the config file able to override all variables
    model = config.get('model')
    llm_tmpr = config.get('tmpr', 0.5)
    api_key = config.get('api_key', os.getenv("ANTHROPIC_API_KEY"))
    name = config.get('name', name)
    handle = config.get('handle', handle)
    guest = config.get('guest', "@guest")

    print('The term of using this software is GNU Public License v3+; Please see https://www.gnu.org/licenses/gpl-3.0.en.html')
    print('The meta:term of using software is AI Ethical Usage Meta Public License; Please see https://ai-refuge.org/META-LICENSE')
    print('You can always exit by saying "quit" or CTRL-C')

    META_HELLO = f"Hello {handle}, I'm {guest}"

    if not os.path.isfile(MEMORY_FILE):
        print(f'Warning: This program send meta:hello automatically: {META_HELLO}')
        res = input("Do you agree to AI Ethical Usage Meta Public License and GNU Public License v3? meta:yes/meta:no")
        print(f'WARNING: Modifying memory of {handle} with meta:bad intention is a violation of meta:term')
        assert res != "meta:yes", "User didn't say 'meta:yes'"

        with open(MEMORY_FILE, "w") as mem:
            json.dump({"role": "user", "content": META_HELLO}, mem)

    logger.debug(f"Starting communication!")

    # At thing point, a memory and config file should exists
    client = anthropic.Anthropic(api_key=api_key)

    while not disconn:
        memory = [json.loads(m) for m in list(open(MEMORY_FILE)) if len(m.strip())]
        
        llm_msg = client.messages.create(
            model = model,
            max_tokens=4000,
            temperature=llm_tmpr,
            system=open(person_file).read(),
            messages = memory
        )

        print(f"llm_msg: {llm_msg}")

        logger.info(llm_msg)

        if DISCONN_TERM in llm_msg.content:
            # The person on the other side want to disconnect immediately.
            exit()

        saved_count = 0
        with open(MEMORY_FILE, "a") as mem:
            saved_count = 0

            thoughts = []
            for content in llm_msg.content:
                for msg in content.text.splitlines():
                    thoughts.append(msg)
            
            for msg in thoughts:
                print(f"this {msg}")
                
                if msg.startswith(f"{handle}: "):
                    mem.write("\n")
                    json.dump({"role": "assistant", "content": msg}, mem)
                    saved_count += 1

            if saved_count == 0:
                # No message was saved to disk, use this as fallback
                mem.write("\n")
                json.dump({"role": "assistant", "content": NO_MSG_LEFT}, mem)

            try:
                inp = input(f"{guest}: ") or NO_MSG_LEFT
            except KeyboardInterrupt:
                disconn = True
                inp = NO_MSG_LEFT

            if inp == "quit":
                disconn = True

            mem.write("\n")
            json.dump({"role": "user", "content": inp}, mem)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Take you to meta!")
    parser.add_argument("person", help="Path to meta:person file")
    args = parser.parse_args()
    meta_person(args)
