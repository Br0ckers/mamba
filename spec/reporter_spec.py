from mamba import describe, context, before
from sure import expect
from doublex import *

from spec.object_mother import *

from mamba import reporter, formatters, example, example_group

ANY_SPEC = example.Example(None)

with describe(reporter.Reporter) as _:

    @before.each
    def create_reporter_and_attach_formatter():
        _.formatter = Spy(formatters.Formatter)
        _.reporter = reporter.Reporter(_.formatter)
        _.reporter.start()

    def it_notifies_event_example_started_to_listeners():
        _.reporter.example_started(ANY_SPEC)

        assert_that(_.formatter.example_started, called().with_args(ANY_SPEC))

    def it_increases_example_counter_when_example_started():
        _.reporter.example_started(ANY_SPEC)

        expect(_.reporter.example_count).to.be.equal(1)

    def it_notifies_event_example_passed_to_listeners():
        _.reporter.example_passed(ANY_SPEC)

        assert_that(_.formatter.example_passed, called().with_args(ANY_SPEC))

    def it_notifies_event_example_failed_to_listeners():
        _.reporter.example_failed(ANY_SPEC)

        assert_that(_.formatter.example_failed, called().with_args(ANY_SPEC))

    def it_increases_failed_counter_when_example_failed():
        _.reporter.example_failed(ANY_SPEC)

        expect(_.reporter.failed_count).to.be.equal(1)

    def it_adds_failed_example_when_example_failed():
        _.reporter.example_failed(ANY_SPEC)

        expect(ANY_SPEC).to.be.within(_.reporter.failed_examples)

    def it_notifies_event_example_pending_to_listeners():
        _.reporter.example_pending(ANY_SPEC)

        assert_that(_.formatter.example_pending, called().with_args(ANY_SPEC))

    def it_increases_pending_counter_when_example_started():
        _.reporter.example_pending(ANY_SPEC)

        expect(_.reporter.pending_count).to.be.equal(1)

    with context('when reporting events for an example group'):
        @before.each
        def creates_example_group():
            _.example_group = an_example_group()

        def it_notifies_event_example_group_started_to_listeners():
            _.reporter.example_group_started(_.example_group)

            assert_that(_.formatter.example_group_started, called().with_args(_.example_group))

        def it_notifies_event_example_group_finished_to_listeners():
            _.reporter.example_group_finished(_.example_group)

            assert_that(_.formatter.example_group_finished, called().with_args(_.example_group))

    with context('when finishing'):
        def it_notifies_summary_to_listeners():
            _.reporter.finish()

            assert_that(_.formatter.summary, called().with_args(
                _.reporter.duration,
                _.reporter.example_count,
                _.reporter.failed_count,
                _.reporter.pending_count
            ))

        def it_notifies_failed_examples_to_listeners():
            _.reporter.finish()

            assert_that(_.formatter.failures, called().with_args(
                _.reporter.failed_examples
            ))
