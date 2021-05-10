from util import command_util
from testcase_parent import ParentTestCase



class CommandUtilityTestCase(ParentTestCase):
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        super(CommandUtilityTestCase, cls).setUpClass()

    def test_invoke(self):
        return_code = command_util.invoke_process(["echo", "foo",'>','/dev/null'])
        self.assertEqual(return_code,0,"Did not invoke trivial process")

