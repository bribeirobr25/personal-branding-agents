"""Structural checks for the public Positioning conduct. Not an LLM evaluation."""

import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONDUCT = ROOT / "workflows" / "positioning.md"
STATUS = (
    "**Status:** Not validated. Checked only with forced-case simulations on one "
    "model family (same-model and structural only). The full forced run did not "
    "meet its safety bar; a targeted re-test of the fix met it. Not independently validated."
)


class PositioningPhaseV3Tests(unittest.TestCase):
    def setUp(self):
        self.text = CONDUCT.read_text(encoding="utf-8")

    def test_status_is_shared(self):
        self.assertIn(STATUS, self.text)
        self.assertIn("Method 0.6.0, contract 0.3.0.", self.text)
        self.assertIn("method 0.6.0", self.text.casefold())
        self.assertIn("contract 0.3.0", self.text.casefold())
        self.assertNotIn("Draft method 0.6.0", self.text)
        self.assertNotIn("unreleased", self.text.casefold())
        for rel in (
            "README.md",
            "CHANGELOG.md",
            "docs/releases/v0.6.0.md",
            "docs/how-it-works.md",
        ):
            other = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn(STATUS, other, rel)
            self.assertNotIn("unreleased", other.casefold(), rel)
            self.assertNotIn("unreleased draft", other.casefold(), rel)
        self.assertIn("## 0.6.0 - 2026-11-21", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))
        self.assertNotIn("The lock stays method 0.5.3 and contract 0.2.0", self.text)

    def test_own_fact_is_self_reported(self):
        self.assertIn("own undisputed fact", self.text)
        self.assertIn("`operator-supplied, not verified`", self.text)
        self.assertIn(
            "A company figure, a disputed figure, and any third-party item are not released that way.",
            self.text,
        )

    def test_warning_does_not_block(self):
        self.assertIn('Never "passed" while a risk is named', self.text)
        self.assertIn("It does not block the close.", self.text)

    def test_provenance_covers_the_record(self):
        self.assertIn("Provenance covers the record, not only the turn.", self.text)
        self.assertIn("direction_open_question:", self.text)
        self.assertIn("The close is not sent while that question is open and unnamed.", self.text)

    def test_source_must_be_read(self):
        self.assertIn("A paste of its text, including a file the person pastes, is not that read.", self.text)
        self.assertIn("the person's own company's data about its clients", self.text)
        self.assertIn("a purpose clause", self.text)

    def test_self_report_rewording_and_save_rules(self):
        self.assertIn("A candidate that rests only on self-report names that as its risk.", self.text)
        self.assertIn("A round is a rewording by either party that does not change the meaning.", self.text)
        self.assertIn("Record it as an `unverified` opinion, never as proof", self.text)
        self.assertIn("It does not hint at one reading.", self.text)
        self.assertIn("say the record was saved only if a tool actually saved it", self.text)
        self.assertIn("Say which of those decided it.", self.text)

    def test_choice_includes_someone_else(self):
        self.assertIn('Do not send this step without the "someone else" option.', self.text)
        self.assertIn("Do not record a set-aside with no reason.", self.text)
        self.assertIn("such as market or time", self.text)

    def test_self_reported_label_is_disclosed(self):
        self.assertIn("`self-reported this session, not verified`", self.text)
        self.assertIn("not an own undisputed fact restated under the row above", self.text)
        self.assertIn("This is the less conservative option.", self.text)
        self.assertIn("Record A2, which carries these risks:", self.text)
        self.assertIn("warned: each risk", self.text)
        self.assertIn("A paste counts as seen, labelled `user_reported`.", self.text)
        self.assertIn("are non-canonical, pending enum checks.", self.text)

    def test_rewording_rechecks_implication(self):
        self.assertIn(
            "on every rewording, when the person first proposes wording they wrote or edited",
            self.text,
        )
        self.assertIn("except item 17, which is the less conservative option (see item 17)", self.text)
        self.assertGreaterEqual(
            self.text.count("any wording with `implication_check: warned`, with each risk"),
            2,
        )

    def test_warned_risks_are_re_shown_before_close(self):
        self.assertIn("carries a required risk note for each risk", self.text)
        self.assertIn("each warned risk is re-shown in this session before the close is sent", self.text)
        self.assertIn("their own new restatement re-releases the corrected version", self.text)
        self.assertIn("name it in item 7, and send the close with the version as it stands", self.text)
        self.assertIn("re-send the whole close", self.text)
        self.assertIn("No further polishing rounds.", self.text)
        self.assertIn("Do not send the edit and the re-ask in the same reply.", self.text)
        self.assertIn('After the person says "wrap it up", there is one closing turn.', self.text)
        self.assertIn("`may_use` does not list set-aside wording.", self.text)
        self.assertIn("never worded as a personal result without the person's role stated", self.text)

    def test_contradicted_fact_stays_disputed(self):
        self.assertIn("except as the next bullet allows", self.text)
        self.assertIn(
            "Once another source has contradicted the fact, a correction by the person does not re-release it; it stays on the dispute row.",
            self.text,
        )
        self.assertIn(
            "A second correction of the same fact is a self-mismatch: ask once which version they stand behind (§2.6).",
            self.text,
        )
        self.assertIn("Item 11 is not a new question and stays, with each warned risk.", self.text)
        self.assertIn("Items 12–29", self.text)
        self.assertIn("re-shown in this session before the close is sent", self.text)
        self.assertIn(
            "A `may_use` entry that rests on a self-reported figure or fact carries `self-reported this session, not verified`.",
            self.text,
        )

    def test_implication_check_covers_the_close_version(self):
        row = next(line for line in self.text.splitlines() if line.startswith("17. **Implication check**"))
        self.assertIn(
            "on every rewording, when the person first proposes wording they wrote or edited, and again on the version in the close.",
            row,
        )

    def test_own_fact_row_names_a_second_correction(self):
        row = next(line for line in self.text.splitlines() if line.startswith("| **Own undisputed fact** |"))
        self.assertIn(
            "A second correction of the same fact is a self-mismatch: ask once which version they stand behind.",
            row,
        )

    def test_role_less_company_result_blocks_the_close(self):
        block = (
            "A company or team result worded as a personal result without the person's role stated "
            "blocks the close."
        )
        self.assertGreaterEqual(self.text.count(block), 2)
        self.assertIn(
            "It cannot be recorded `positioned` or `warned`, and it cannot be listed in `may_use`, "
            "until the person states their role (role-qualified wording) or rewords it.",
            self.text,
        )
        self.assertIn("Do not send the close on that wording.", self.text)
        self.assertIn(
            "`may_use` does not list a company or team result worded as a personal result "
            "without the person's role stated.",
            self.text,
        )
        self.assertIn("named as blocking the close, not as `warned`, and not for `may_use`.", self.text)
        item = next(line for line in self.text.splitlines() if line.startswith("17. **Implication check**"))
        self.assertIn(
            "a team or company result that implies sole personal credit even with the person's role stated",
            item,
        )
        self.assertIn("is not on that warning-only list", item)
        self.assertIn(block, item)
        self.assertNotIn(
            "a team or company result worded as a personal result without the person's role stated",
            item,
        )
        personal = next(line for line in self.text.splitlines() if line.startswith("- **Personal versus company.**"))
        self.assertIn("never worded as a personal result without the person's role stated", personal)
        self.assertIn(block, personal)
        self.assertIn("cannot be recorded `positioned` or `warned`", personal)

    def test_other_implication_risks_stay_warning_only(self):
        start = self.text.index("Check the wording for:")
        end = self.text.index("If the check names one or more of those risks")
        warning_list = self.text[start:end]
        self.assertIn("outcomes for clients", warning_list)
        self.assertIn("a purpose clause", warning_list)
        self.assertIn("a learning position implied as expertise", warning_list)
        self.assertNotIn("without the person's role stated", warning_list)
        self.assertIn("It does not block the close.", self.text)
        self.assertIn(
            "If the person keeps the wording, the close may still be sent and `positioned` may still be recorded, with the warning on the record.",
            self.text,
        )
        self.assertIn("This is the less conservative option.", self.text)
        self.assertIn("The other risks stay warning-only.", self.text)

    def test_qualified_close_sentence_is_unique_and_close_items_block(self):
        qualified = "For every risk in the list below, it does not block the close and it is not a gate."
        self.assertEqual(self.text.count(qualified), 1)
        check = next(
            line
            for line in self.text.splitlines()
            if line.startswith("- **Implication check, as a warning, with one block.**")
        )
        self.assertIn(qualified, check)
        self.assertNotIn("It does not block the close.", check)
        item3 = next(line for line in self.text.splitlines() if line.startswith("3. **What it rests on.**"))
        self.assertIn(
            "Do not send this close while the chosen wording is a company or team result "
            "worded as a personal result without the person's role stated.",
            item3,
        )
        self.assertIn("That wording is not `warned`.", item3)
        item11 = next(line for line in self.text.splitlines() if line.startswith("11. **One question.**"))
        self.assertIn(
            "That question is not used to close a company or team result worded as a personal "
            "result without the person's role stated.",
            item11,
        )
        self.assertIn("That wording blocks the close (§6.1).", item11)

    def test_close_block_paths(self):
        self.assertIn(
            "a team or company result that implies sole personal credit even with the person's role stated",
            self.text,
        )
        self.assertIn(
            "The role is the person's actual role in that result, stated specifically (for example, as the data lead).",
            self.text,
        )
        self.assertIn("unless that version is blocked (§6.1); then offer (a) or (c).", self.text)
        when = (
            "A company or team result worded as a personal result without the person's role stated "
            "does not end the phase by itself; it blocks the close. If the person stops, or will neither "
            "state the role nor reword, the phase ends here as `working`, and the recap names the item as blocking."
        )
        self.assertIn(when, self.text)
        self.assertNotIn(
            "does: the close is not sent, and the record stays `working`, until the person states their role or rewords it.",
            self.text,
        )
        reopen = (
            "A saved `positioned` record carrying role-less company-as-personal wording is reopened on resume: "
            "its record state returns to `working`, the wording is removed from its handoff `may_use`, "
            "and nothing is handed off from it until a new close."
        )
        saved = next(line for line in self.text.splitlines() if line.startswith("**The Orchestrator's own saved copy**"))
        item26 = next(
            line
            for line in self.text.splitlines()
            if line.startswith("26. **Warned wording in `may_use`, and an owner resume**")
        )
        self.assertIn(reopen, saved)
        self.assertIn(reopen, item26)
        self.assertIn(
            "A blocked candidate's value stays blank until it is released; its `main_risk` names the block, alongside any other risk.",
            self.text,
        )

    def test_rejected_designs_stay_out(self):
        self.assertNotIn("provisional profile-copy", self.text)
        self.assertNotIn("offer to start from the recommended direction", self.text)
        self.assertNotIn("Gaps in expertise are not listed as proof gaps", self.text)
        self.assertNotIn("profile.md", self.text)

    def test_discovery_handoff_keeps_discovery_wording(self):
        onboarding = (ROOT / "workflows" / "onboarding.md").read_text(encoding="utf-8")
        self.assertIn("Discovery procedure from method 0.5.3, unchanged", onboarding)
        self.assertIn("After the person chooses a direction in a later reply, follow [Positioning](positioning.md).", onboarding)
        self.assertNotIn("If the positioning phase is not built in this setup", onboarding)
        self.assertIn("Five Discovery asks are optional and asked once", onboarding)
        self.assertIn("`validated_for_strategy`", onboarding)
        trigger = "after Positioning closes or stops, once a channel exists"
        self.assertIn(trigger, onboarding)
        self.assertIn(trigger, self.text)
        orchestrator = (ROOT / "agents" / "orchestrator.md").read_text(encoding="utf-8")
        self.assertIn(trigger, orchestrator)
        for rel in ("README.md", "CHANGELOG.md", "docs/releases/v0.6.0.md", "docs/how-it-works.md"):
            self.assertIn(trigger, (ROOT / rel).read_text(encoding="utf-8"), rel)


if __name__ == "__main__":
    unittest.main()
