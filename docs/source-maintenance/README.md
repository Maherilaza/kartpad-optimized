# Maintaining WiiCompiled source

WiiCompiled is created by [patchzyy and contributors](https://github.com/patchzyy/wiicompiled).
KartPad's editable translator is in [`vendor/wiicompiled/translator`](../../vendor/wiicompiled/translator).
Edit those files directly. `scripts/prepare-patched-translator.sh` retains its
historical name and output location but now stages source without applying patches.
The staged `runtime/src` used for native registration remains the upstream baseline.

The subtree was imported from WiiCompiled commit
`1912292c804ff9b1b79938de89369ec4496f9fff`, tree
`34f9deda094915e12f47316059911b28c6812964`. Its original license, README and
component notices remain inside the subtree; KartPad's top-level notices still
apply. Upstream identity and the maintained source location are recorded in
`dependencies.lock.json`. The subtree history records the upstream split commit.

**Migration is in progress.** Runtime/Aurora app preparation still uses the
existing platform patch stacks. Their imported source is not yet the app build
input. Do not edit that imported runtime and assume it affects shipped apps.
The eight old translator patches are retained temporarily as migration evidence;
normal translator preparation no longer reads them. They are not a second place
to maintain translator fixes.

## Upstream comparisons and contributions

Fetch the recorded upstream base before comparing source:

```sh
git fetch https://github.com/patchzyy/wiicompiled.git 1912292c804ff9b1b79938de89369ec4496f9fff
git subtree split --prefix=vendor/wiicompiled -b review/wiicompiled-source
git diff 1912292c804ff9b1b79938de89369ec4496f9fff review/wiicompiled-source -- translator
```

For a contribution, start a branch at the appropriate upstream revision in your
actual GitHub fork of WiiCompiled. Transfer only the specific fix and its tests,
then test that branch against upstream. Do not submit the whole KartPad port delta
as one fix. The source subtree makes comparison possible; it does not attach
KartPad itself to GitHub's fork network or create a contributor fork automatically.

Rehearse upstream updates in a disposable checkout using `git subtree pull
--prefix=vendor/wiicompiled --squash <upstream-url> <reviewed-revision>`. Record and
review the new pin only after resolving changes and validating affected consumers.
Do not update upstream as part of the current layout migration.

See [migration and rollback gates](MIGRATION.md) and [validation](VALIDATION.md).
