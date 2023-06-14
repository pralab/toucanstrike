import cmd2
from cmd2 import Cmd
import sys
from io import StringIO

from commands.blackbox import get_black_box_parser, blackbox
from commands.clear import clear
from commands.data import get_data_parser, data
from commands.predict import get_predict_parser, predict
from commands.run import get_run_parser, run
from commands.set import do_set_atk, get_set_atk_parser
from commands.status import status
from commands.target import target, get_target_parser
from commands.whitebox import get_white_box_parser, whitebox
from constants import TOUCAN_STRIKE_COMMANDS
from prompts import get_default_prompt


class ToucanStrikeInterface(Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = get_default_prompt()

    # Override the onecmd method to capture the output
    def onecmd(self, line):
        stdout_saved = sys.stdout
        sys.stdout = StringIO()  # Create a StringIO object to capture the output
        try:
            return super().onecmd(line)
        finally:
            output = sys.stdout.getvalue()  # Get the captured output
            sys.stdout.close()
            sys.stdout = stdout_saved
            return output

    @cmd2.with_argparser(get_white_box_parser())
    @cmd2.with_category(TOUCAN_STRIKE_COMMANDS)
    def do_whitebox(self, args):
        """
        Setup a white-box attack.
        """
        whitebox(args)

    @cmd2.with_argparser(get_black_box_parser())
    @cmd2.with_category(TOUCAN_STRIKE_COMMANDS)
    def do_blackbox(self, args):
        """
        Setup a black-box attack.
        """
        blackbox(args)

    @cmd2.with_argparser(get_target_parser())
    @cmd2.with_category(TOUCAN_STRIKE_COMMANDS)
    def do_target(self, args):
        """Set attack target"""
        target(args)

    @cmd2.with_category(TOUCAN_STRIKE_COMMANDS)
    def do_status(self, args):
        """Print current set up of the attack"""
        status()

    @cmd2.with_argparser(get_run_parser())
    @cmd2.with_category(TOUCAN_STRIKE_COMMANDS)
    def do_run(self, args):
        """Run the specified attack against the target, using the specified data"""
        run(args)

    @cmd2.with_argparser(get_predict_parser())
    @cmd2.with_category(TOUCAN_STRIKE_COMMANDS)
    def do_predict(self, args):
        """Compute prediction of a sample, using the already set target"""
        predict(args)

    @cmd2.with_argparser(get_data_parser())
    @cmd2.with_category(TOUCAN_STRIKE_COMMANDS)
    def do_data(self, args):
        """Set the data for attack and prediction"""
        data(args)

    @cmd2.with_category(TOUCAN_STRIKE_COMMANDS)
    def do_clear(self, args):
        """Clear all the information stored for the attack"""
        clear()

    @cmd2.with_argparser(get_set_atk_parser())
    @cmd2.with_category(TOUCAN_STRIKE_COMMANDS)
    def do_setatk(self, args):
        """Set the parameters for the attack"""
        do_set_atk(args)
