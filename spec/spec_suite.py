from mamba import describe, context
from sure import expect

from mamba.spec import Spec, Suite

IRRELEVANT_SUBJECT = 'irrelevant_subject'


with describe('Suite') as _:

    def it_should_have_same_name_than_subject():
        suite = Suite(IRRELEVANT_SUBJECT)

        expect(suite.name).to.be.equals(IRRELEVANT_SUBJECT)

    def it_should_have_depth_greater_than_parent():
        test = Spec(_test)
        suite = Suite(IRRELEVANT_SUBJECT)
        suite.append(test)

        expect(test.depth).to.be.equal(1)

    with context('#run'):
        def _test():
            _.was_run = True

        def it_should_run_the_test():
            suite = Suite(IRRELEVANT_SUBJECT)
            suite.append(Spec(_test))
            suite.append(Spec(_test))

            suite.run()

            expect(_.was_run).to.be.true

        def it_should_calculate_elapsed_time():
            suite = Suite(IRRELEVANT_SUBJECT)
            suite.append(Spec(_test))
            suite.append(Spec(_test))

            suite.run()

            expect(suite.elapsed_time.total_seconds()).to.be.greater_than(0)

