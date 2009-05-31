# -*- coding: utf-8 -*-

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import urllib2

from test_fixture import *
from common import force_unicode
from terminal_colored import *

class StoryRunner(object):
    def __init__(self, browser_driver):
        self.browser_driver = browser_driver
        self.term = TerminalController()

    def run_stories(self, context):
        self.context = context
        test_fixture = context.test_fixture

        #No tests to run
        if len(test_fixture.stories) == 0:
            test_fixture.did_not_run()
            return

        base_url = None
        if self.context.base_url:
            protocol, page_name, file_name, complement, querystring, anchor = urllib2.urlparse.urlparse(self.context.base_url)
            base_url = protocol and self.context.base_url or None

        if base_url:
            self.browser_driver.start_test(base_url)
        else:
            self.browser_driver.start_test()

        try:
            test_fixture.start_run()
            for current_story in test_fixture.stories:
                self.raise_pre_story(context, current_story)
                self.__run_scenarios(current_story, context)
                self.raise_post_story(context, current_story, current_story.status)
        finally:
            test_fixture.end_run()
            self.browser_driver.stop_test()

    def __run_scenarios(self, current_story, context):
        for current_scenario in current_story.scenarios:
            # running only the given scenarios
            scenarios = None
            if context.scenarios_to_run:
                scenarios = context.scenarios_to_run.replace(" ", "").split(",")
                if current_scenario.index not in scenarios:
                    continue

            self.raise_pre_scenario(context, current_story, current_scenario)
            current_scenario.start_run()
            for current_action in (current_scenario.givens + current_scenario.whens + current_scenario.thens):
                current_action.start_run()
                result = current_action.execute(context)
                current_action.end_run()
                if not result:
                    break
            current_scenario.end_run()
            self.raise_post_scenario(context, current_story, current_scenario, current_scenario.status)

    def raise_pre_story(self, context, story):
        self.__msg_pre_story(context, story)
        conditions = story.conditions_module
        if conditions and hasattr(conditions, "pre_story"):
            conditions.pre_story(context, story)

    def raise_post_story(self, context, story, result):
        self.__msg_post_story(context, story)
        conditions = story.conditions_module
        if conditions and hasattr(conditions, "post_story"):
            conditions.post_story(context, story, result)

    def raise_pre_scenario(self, context, story, scenario):
        self.__msg_pre_scenario(context, scenario)
        conditions = story.conditions_module
        if conditions and hasattr(conditions, "pre_scenario"):
            conditions.pre_scenario(context, story, scenario)

    def raise_post_scenario(self, context, story, scenario, result):
        self.__msg_post_scenario(context, scenario)
        conditions = story.conditions_module
        if conditions and hasattr(conditions, "post_scenario"):
            conditions.post_scenario(context, story, scenario, result)

    def __msg_pre_story(self, context, story):
        messages = []
        messages.append("=" * 80)
        messages.append("%s" % context.language["story"])
        messages.append("\n   %s %s\n   %s %s\n   %s %s\n" % (context.language["as_a"], force_unicode(story.as_a),
                                                       context.language["i_want_to"], force_unicode(story.i_want_to),
                                                       context.language["so_that"], force_unicode(story.so_that)))
        print self.term.render(u"\n".join(messages))

    def __msg_post_story(self, context, story):
        messages = []
        messages.append("-" * 80)
        if story.status == 'SUCCESSFUL':
            color = 'GREEN'
        elif story.status == 'FAILED':
            color = 'BG_RED'
        else:
            color = 'CYAN'
        messages.append("${%s}%s: %s${NORMAL}" % (color, context.language["story_status"], story.status))
        messages.append("-" * 80)
        messages.append("")
        
        print self.term.render(u"\n".join(messages))

    def __msg_pre_scenario(self, context, scenario):
        messages = []
        messages.append("-" * 80)
        messages.append(u"%s %s - %s" % (context.language["scenario"], force_unicode(scenario.index), force_unicode(scenario.title)))
        messages.append("-" * 80)
        messages.append("")

        print self.term.render(u"\n".join(messages))

    def __msg_post_scenario(self, context, scenario):
        messages = []

        messages.append("   ${YELLOW}%s: ${NORMAL}" % context.language["given"])
        for given in scenario.givens:
            if given.status == 'SUCCESSFUL':
                color = 'GREEN'
            elif given.status == 'FAILED':
                color = 'BG_RED'
            else:
                color = 'CYAN'
            messages.append("      ${%s}%s - %s${NORMAL}" % (color, given.description, given.status))

        messages.append("   ${YELLOW}%s: ${NORMAL}" % context.language["when"])
        for when in scenario.whens:
            if when.status == 'SUCCESSFUL':
                color = 'GREEN'
            elif when.status == 'FAILED':
                color = 'BG_RED'
            else:
                color = 'CYAN'
            messages.append("      ${%s}%s - %s${NORMAL}" % (color, when.description, when.status))

        messages.append("${YELLOW}   %s: ${NORMAL}" % context.language["then"])
        for then in scenario.thens:
            if then.status == 'SUCCESSFUL':
                color = 'GREEN'
            elif then.status == 'FAILED':
                color = 'BG_RED'
            else:
                color = 'CYAN'
            messages.append("      ${%s}%s - %s${NORMAL}" % (color, then.description, then.status))

        if scenario.status == 'SUCCESSFUL':
            color = 'GREEN'
        elif scenario.status == 'FAILED':
            color = 'BG_RED'
        else:
            color = 'CYAN'
        messages.append("")
        messages.append("   ${%s}%s: %s${NORMAL}" % (color, context.language["scenario_status"], scenario.status))
        messages.append("")

        print self.term.render(u"\n".join(messages))
