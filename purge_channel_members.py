import argparse
import asyncio
import getpass
import os
from typing import Set

from telethon import TelegramClient, errors, functions, types


SESSION_NAME = "owner_session"


def print_banner() -> None:
    print("")
    print("╔══════════════════════════════════════════════╗")
    print("║        Telegram Channel Member Purger        ║")
    print("║          Safe, stylish, and controlled       ║")
    print("╚══════════════════════════════════════════════╝")
    print("Created by FUNMIG")
    print("")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove channel/supergroup members except your Telegram contacts."
    )
    parser.add_argument(
        "target",
        help="Channel/supergroup username, invite link, or numeric id. Example: @mychannel",
    )
    parser.add_argument("--api-id", type=int, default=os.getenv("TG_API_ID"))
    parser.add_argument("--api-hash", default=os.getenv("TG_API_HASH"))
    parser.add_argument("--phone", default=os.getenv("TG_PHONE"))
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually remove members. Without this flag the script only prints a dry-run.",
    )
    parser.add_argument(
        "--keep-admins",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Keep channel admins too. Default: enabled.",
    )
    parser.add_argument(
        "--ban-instead-of-kick",
        action="store_true",
        help="Keep removed users banned. Default behavior is ban then unban, which kicks them.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between removals in seconds. Increase this for large channels.",
    )
    return parser.parse_args()


async def get_contact_ids(client: TelegramClient) -> Set[int]:
    result = await client(functions.contacts.GetContactsRequest(hash=0))
    return {user.id for user in result.users if isinstance(user, types.User)}


async def get_admin_ids(client: TelegramClient, entity) -> Set[int]:
    admin_ids: Set[int] = set()
    async for user in client.iter_participants(
        entity, filter=types.ChannelParticipantsAdmins
    ):
        if isinstance(user, types.User):
            admin_ids.add(user.id)
    return admin_ids


async def remove_member(client: TelegramClient, entity, user, ban_instead: bool) -> None:
    ban_rights = types.ChatBannedRights(until_date=None, view_messages=True)
    await client(
        functions.channels.EditBannedRequest(
            channel=entity,
            participant=user,
            banned_rights=ban_rights,
        )
    )

    if not ban_instead:
        unban_rights = types.ChatBannedRights(until_date=None, view_messages=False)
        await client(
            functions.channels.EditBannedRequest(
                channel=entity,
                participant=user,
                banned_rights=unban_rights,
            )
        )


async def main() -> None:
    args = parse_args()
    print_banner()

    api_id = args.api_id or input("TG_API_ID: ").strip()
    api_hash = args.api_hash or getpass.getpass("TG_API_HASH: ").strip()
    phone = args.phone or input("Phone number, e.g. +98912...: ").strip()

    client = TelegramClient(SESSION_NAME, int(api_id), api_hash)
    await client.start(phone=phone)

    me = await client.get_me()
    entity = await client.get_entity(args.target)

    contact_ids = await get_contact_ids(client)
    protected_ids = set(contact_ids)
    protected_ids.add(me.id)

    if args.keep_admins:
        protected_ids.update(await get_admin_ids(client, entity))

    print(f"Logged in as: {me.id} / {getattr(me, 'username', None)}")
    print(f"Target: {getattr(entity, 'title', args.target)}")
    print(f"Contacts protected: {len(contact_ids)}")
    print(f"Mode: {'EXECUTE' if args.execute else 'DRY-RUN'}")

    checked = 0
    protected = 0
    removed = 0
    failed = 0

    async for user in client.iter_participants(entity):
        if not isinstance(user, types.User):
            continue

        checked += 1
        label = f"{user.id} @{user.username}" if user.username else str(user.id)

        if user.id in protected_ids:
            protected += 1
            print(f"KEEP   {label}")
            continue

        if not args.execute:
            removed += 1
            print(f"WOULD REMOVE {label}")
            continue

        try:
            await remove_member(client, entity, user, args.ban_instead_of_kick)
            removed += 1
            print(f"REMOVE {label}")
            await asyncio.sleep(args.delay)
        except errors.FloodWaitError as exc:
            wait_for = int(exc.seconds) + 3
            print(f"Flood wait: sleeping {wait_for} seconds")
            await asyncio.sleep(wait_for)
        except errors.UserAdminInvalidError:
            failed += 1
            print(f"FAIL   {label} - not enough admin/owner permission")
        except errors.ChatAdminRequiredError:
            failed += 1
            print("FAIL   Telegram says admin rights are required. Stopping.")
            break
        except Exception as exc:
            failed += 1
            print(f"FAIL   {label} - {type(exc).__name__}: {exc}")

    print("")
    print("Summary")
    print(f"Checked:   {checked}")
    print(f"Protected: {protected}")
    print(f"Removed:   {removed if args.execute else 0}")
    print(f"Dry-run removals: {removed if not args.execute else 0}")
    print(f"Failed:    {failed}")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
