#!/bin/sh
set -eu

umask 077

REPO_ROOT=/Users/chenjie/Documents/MES/edge-mes-demo
EXPECTED_BRANCH=main
EXPECTED_COMMIT=8de5edbb504538a233abbcc80102cb714c9cee65
EXPECTED_BLOB=b46a637f23c761d0a4c3fe048b3b7480a3dec2ce
EXPECTED_BYTES=7112
EXPECTED_SHA256=d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d
TARGET_RELATIVE=config/mapping.yaml

fail() {
    printf 'HOLD / NO MATERIALIZATION: %s\n' "$1" >&2
    exit 2
}

test "$(git -C "$REPO_ROOT" rev-parse --show-toplevel)" = "$REPO_ROOT" || fail "unexpected Git root"
test "$(git -C "$REPO_ROOT" branch --show-current)" = "$EXPECTED_BRANCH" || fail "branch drift"
test "$(git -C "$REPO_ROOT" rev-parse HEAD)" = "$EXPECTED_COMMIT" || fail "HEAD drift"
test "$(git -C "$REPO_ROOT" rev-parse origin/main)" = "$EXPECTED_COMMIT" || fail "origin/main drift"

set -- $(git -C "$REPO_ROOT" rev-list --left-right --count HEAD...origin/main)
test "$#" -eq 2 || fail "ahead/behind shape drift"
test "$1" -eq 0 || fail "checkout is ahead"
test "$2" -eq 0 || fail "checkout is behind"
printf 'AHEAD_BEHIND=%s\t%s\n' "$1" "$2"

test -z "$(git -C "$REPO_ROOT" diff --cached --name-only)" || fail "cached changes present"
git -C "$REPO_ROOT" diff --quiet -- "$TARGET_RELATIVE" || fail "mapping working tree is dirty"

git -C "$REPO_ROOT" cat-file -e "$EXPECTED_COMMIT:$TARGET_RELATIVE" || fail "Git object absent"
test "$(git -C "$REPO_ROOT" rev-parse "$EXPECTED_COMMIT:$TARGET_RELATIVE")" = "$EXPECTED_BLOB" || fail "blob drift"

temp_root="$(mktemp -d "${TMPDIR:-/tmp}/d2-r7b-p2-r2.XXXXXX")"
normalized_root="$(cd "$temp_root" && pwd -P)"
case "$normalized_root" in
    */d2-r7b-p2-r2.*) ;;
    *) fail "temporary parent normalization outside bounded contract" ;;
esac

mkdir -p "$normalized_root/config"
materialized="$normalized_root/$TARGET_RELATIVE"
git -C "$REPO_ROOT" cat-file -p "$EXPECTED_COMMIT:$TARGET_RELATIVE" > "$materialized"

actual_bytes="$(wc -c < "$materialized" | tr -d ' ')"
actual_sha256="$(shasum -a 256 "$materialized" | awk '{print $1}')"
actual_blob="$(git -C "$REPO_ROOT" hash-object "$materialized")"
test "$actual_blob" = "$EXPECTED_BLOB" || fail "materialized blob drift"
test "$actual_bytes" -eq "$EXPECTED_BYTES" || fail "materialized byte drift"
test "$actual_sha256" = "$EXPECTED_SHA256" || fail "materialized SHA-256 drift"

printf 'TEMP_ROOT=%s\n' "$normalized_root"
printf 'MATERIALIZED_PATH=%s\n' "$materialized"
printf 'BLOB=%s\n' "$actual_blob"
printf 'BYTES=%s\n' "$actual_bytes"
printf 'SHA256=%s\n' "$actual_sha256"
printf 'NO_AUTO_CLEANUP=1\n'
printf 'BOUNDED_CLEANUP_CONTRACT=caller may remove only this normalized exact root after review; no glob cleanup\n'
