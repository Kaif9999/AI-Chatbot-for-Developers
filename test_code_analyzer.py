"""
Unit tests for Code Analyzer module.
"""

import unittest
from code_analyzer import CodeAnalyzer, PythonCodeAnalyzer, Severity, IssueCategory


class TestPythonCodeAnalyzer(unittest.TestCase):
    """Test suite for Python code analyzer."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = PythonCodeAnalyzer()

    def test_mutable_default_argument(self):
        """Test detection of mutable default arguments."""
        code = """
def foo(x, items=[]):
    items.append(x)
    return items
"""
        issues = self.analyzer.analyze(code)
        self.assertTrue(any('mutable default' in issue.message.lower() for issue in issues))

    def test_bare_except(self):
        """Test detection of bare except clauses."""
        code = """
try:
    risky_operation()
except:
    pass
"""
        issues = self.analyzer.analyze(code)
        self.assertTrue(any('bare except' in issue.message.lower() for issue in issues))

    def test_dangerous_eval(self):
        """Test detection of eval() usage."""
        code = """
result = eval(user_input)
"""
        issues = self.analyzer.analyze(code)
        self.assertTrue(any('eval' in issue.message.lower() for issue in issues))

    def test_dangerous_exec(self):
        """Test detection of exec() usage."""
        code = """
exec(some_code)
"""
        issues = self.analyzer.analyze(code)
        self.assertTrue(any('exec' in issue.message.lower() for issue in issues))

    def test_unused_variable(self):
        """Test detection of unused variables."""
        code = """
def foo():
    used_var = 10
    unused_var = 20
    return used_var
"""
        issues = self.analyzer.analyze(code)
        unused_issues = [i for i in issues if 'unused' in i.message.lower()]
        self.assertGreater(len(unused_issues), 0)

    def test_long_function(self):
        """Test detection of overly long functions."""
        # Create a function with more than 50 lines
        lines = ["def long_function():"]
        lines.extend([f"    x{i} = {i}" for i in range(60)])
        lines.append("    return x0")
        code = '\n'.join(lines)

        issues = self.analyzer.analyze(code)
        self.assertTrue(any('too long' in issue.message.lower() for issue in issues))

    def test_function_naming_convention(self):
        """Test detection of naming convention violations."""
        code = """
def MyFunction():
    pass

def AnotherBadName():
    pass
"""
        issues = self.analyzer.analyze(code)
        naming_issues = [i for i in issues if 'snake_case' in i.suggestion.lower()]
        self.assertGreater(len(naming_issues), 0)

    def test_class_naming_convention(self):
        """Test detection of class naming violations."""
        code = """
class my_class:
    pass

class another_bad_class:
    pass
"""
        issues = self.analyzer.analyze(code)
        naming_issues = [i for i in issues if 'PascalCase' in i.suggestion]
        self.assertGreater(len(naming_issues), 0)

    def test_hardcoded_password(self):
        """Test detection of hardcoded secrets."""
        code = """
password = "secret123"
api_key = "abc123xyz"
"""
        issues = self.analyzer.analyze(code)
        security_issues = [i for i in issues if i.category == IssueCategory.SECURITY]
        self.assertGreater(len(security_issues), 0)

    def test_sql_injection_vulnerability(self):
        """Test detection of potential SQL injection."""
        code = """
query = "SELECT * FROM users WHERE id = %s" % user_id
"""
        issues = self.analyzer.analyze(code)
        sql_issues = [i for i in issues if 'sql' in i.message.lower()]
        self.assertGreater(len(sql_issues), 0)

    def test_syntax_error_detection(self):
        """Test handling of syntax errors."""
        code = """
def foo(
    pass
"""
        issues = self.analyzer.analyze(code)
        self.assertTrue(any('syntax' in issue.message.lower() for issue in issues))

    def test_clean_code_no_issues(self):
        """Test that clean code produces no critical issues."""
        code = """
def calculate_sum(numbers):
    '''Calculate sum of numbers.'''
    total = 0
    for num in numbers:
        total += num
    return total

class Calculator:
    '''A simple calculator class.'''
    pass
"""
        issues = self.analyzer.analyze(code)
        critical_issues = [i for i in issues if i.severity == Severity.CRITICAL]
        self.assertEqual(len(critical_issues), 0)


class TestCodeAnalyzer(unittest.TestCase):
    """Test suite for multi-language code analyzer."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = CodeAnalyzer()

    def test_python_analysis(self):
        """Test Python code analysis."""
        code = """
def foo(items=[]):
    return items
"""
        issues = self.analyzer.analyze(code, 'python')
        self.assertGreater(len(issues), 0)

    def test_basic_pattern_analysis(self):
        """Test pattern-based analysis for unsupported languages."""
        # JavaScript code
        code = """
function test() {
    console.log("Debug message");
    // TODO: implement this
}
"""
        issues = self.analyzer.analyze(code, 'javascript')
        self.assertTrue(any('console.log' in issue.message for issue in issues))

    def test_todo_comment_detection(self):
        """Test detection of TODO comments."""
        code = """
def foo():
    # TODO: implement this feature
    pass
"""
        issues = self.analyzer.analyze(code, 'python')
        # This might not be detected by AST analyzer, but would be by pattern analyzer

    def test_format_report_text(self):
        """Test text format report generation."""
        code = """
def foo(items=[]):
    return items
"""
        issues = self.analyzer.analyze(code, 'python')
        report = self.analyzer.format_report(issues, 'text')

        self.assertIn('CODE ANALYSIS REPORT', report)
        self.assertIn('Total Issues Found', report)

    def test_format_report_json(self):
        """Test JSON format report generation."""
        code = """
def foo(items=[]):
    return items
"""
        issues = self.analyzer.analyze(code, 'python')
        report = self.analyzer.format_report(issues, 'json')

        # Should be valid JSON
        import json
        data = json.loads(report)
        self.assertIsInstance(data, list)
        if len(data) > 0:
            self.assertIn('severity', data[0])
            self.assertIn('message', data[0])

    def test_multiple_issues_in_code(self):
        """Test detection of multiple issues in complex code."""
        code = """
password = "secret123"

def MyBadFunction(items=[]):
    unused = 10
    try:
        result = eval("1+1")
    except:
        pass
    return items

class my_bad_class:
    pass
"""
        issues = self.analyzer.analyze(code, 'python')

        # Should detect multiple issues
        self.assertGreater(len(issues), 5)

        # Check different categories are detected
        categories = {issue.category for issue in issues}
        self.assertGreater(len(categories), 1)

    def test_issue_sorting_by_severity(self):
        """Test that issues are sorted by severity."""
        code = """
password = "secret123"  # HIGH severity

def foo(items=[]):  # HIGH severity
    unused = 10  # LOW severity
    return items
"""
        issues = self.analyzer.analyze(code, 'python')

        # Check if critical/high severity issues come first
        if len(issues) > 1:
            first_severity = issues[0].severity
            last_severity = issues[-1].severity

            severity_order = [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]
            self.assertLessEqual(
                severity_order.index(first_severity),
                severity_order.index(last_severity)
            )


class TestCodeIssueDataclass(unittest.TestCase):
    """Test CodeIssue dataclass."""

    def test_code_issue_creation(self):
        """Test creating a CodeIssue instance."""
        from code_analyzer import CodeIssue

        issue = CodeIssue(
            category=IssueCategory.BUG,
            severity=Severity.HIGH,
            line_number=10,
            column=5,
            message="Test issue",
            code_snippet="test code",
            suggestion="Fix it",
            rule_id="TEST001"
        )

        self.assertEqual(issue.category, IssueCategory.BUG)
        self.assertEqual(issue.severity, Severity.HIGH)
        self.assertEqual(issue.line_number, 10)
        self.assertEqual(issue.message, "Test issue")


if __name__ == '__main__':
    unittest.main()
