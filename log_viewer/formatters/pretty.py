"""
Pretty formatter with ANSI colors for console output.
"""


class Colors:
    """ANSI color codes."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def format(report):
    """
    Format search results with ANSI colors for console output.
    
    Args:
        report: dict, search report from searcher.search()
        
    Returns:
        str: formatted text with ANSI color codes
    """
    lines = []
    summary = report["summary"]
    results = report["results"]
    
    # Summary section
    lines.append(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}")
    lines.append(f"LOG SEARCH RESULTS{Colors.RESET}")
    lines.append(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.RESET}")
    lines.append("")
    
    lines.append(f"{Colors.GREEN}Matches:{Colors.RESET} {Colors.BOLD}{summary['matches']}{Colors.RESET}")
    lines.append(f"{Colors.GREEN}Total Lines Scanned:{Colors.RESET} {Colors.BOLD}{summary['total_lines']}{Colors.RESET}")
    
    if summary['earliest_timestamp']:
        lines.append(f"{Colors.GREEN}Earliest Timestamp:{Colors.RESET} {Colors.CYAN}{summary['earliest_timestamp']}{Colors.RESET}")
    if summary['latest_timestamp']:
        lines.append(f"{Colors.GREEN}Latest Timestamp:{Colors.RESET} {Colors.CYAN}{summary['latest_timestamp']}{Colors.RESET}")
    
    lines.append("")
    lines.append(f"{Colors.HEADER}{'-' * 70}{Colors.RESET}")
    lines.append("")
    
    # Results section
    if not results:
        lines.append(f"{Colors.YELLOW}No matches found.{Colors.RESET}")
    else:
        for i, result in enumerate(results, 1):
            lines.append(f"{Colors.BOLD}Match #{i}{Colors.RESET}")
            lines.append(f"  {Colors.BLUE}Line Number:{Colors.RESET} {Colors.BOLD}{result['line_number']}{Colors.RESET}")
            lines.append(f"  {Colors.BLUE}Timestamp:{Colors.RESET} {Colors.CYAN}{result['timestamp'] or 'N/A'}{Colors.RESET}")
            lines.append(f"  {Colors.BLUE}Content:{Colors.RESET} {result['line']}")
            lines.append(f"  {Colors.BLUE}Highlighted:{Colors.RESET} {Colors.YELLOW}{result['highlighted']}{Colors.RESET}")
            
            if result['context_before']:
                lines.append(f"  {Colors.BLUE}Context Before:{Colors.RESET}")
                for ctx_line in result['context_before']:
                    lines.append(f"    {Colors.CYAN}| {ctx_line}{Colors.RESET}")
            
            if result['context_after']:
                lines.append(f"  {Colors.BLUE}Context After:{Colors.RESET}")
                for ctx_line in result['context_after']:
                    lines.append(f"    {Colors.CYAN}| {ctx_line}{Colors.RESET}")
            
            lines.append("")
    
    lines.append(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.RESET}")
    
    return "\n".join(lines)
