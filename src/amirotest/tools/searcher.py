from pathlib import Path
import re

FLAG_REGEX = re.compile("([A_Z,0-9,_]+)")
IF_DEFINED_DEFAULT_REGEX = re.compile(
            r'''^\#if\s                                # Match beginning #if
            (defined\(([A-Z,\d,_]+)\)                    # Match defined((FLAG))
            |\(([A-Z,0-9,_]+)\s==\s(TRUE|True|true)\) # Match ((FLAG) == true)
            )
            .*$
            ''',
            re.VERBOSE | re.MULTILINE)

class SearchResult():
    def __init__(self, filepath, results):
        self.filepath = filepath
        self.results = results
        self.flags = self._extract_flags_from_results()

    def _extract_flags_from_results(self) -> list[str]:
        flags = []
        for res in self.results:
            for match in res:
                if FLAG_REGEX.match(match):
                    flags.append(match)
        return flags

class Searcher():
    def search_if_defined_flags(self, module_path) -> list[SearchResult]:
        regex: re.Pattern = IF_DEFINED_DEFAULT_REGEX
        results = self.apply_regex_to_module_path(module_path, regex)
        return results


    def apply_regex_to_module_path(self, searchDir: Path, regex: re.Pattern) -> list[SearchResult]:
        searchResults = []
        for f in searchDir.glob("**/*"):
            if f.is_file():
                with f.open() as f_handle:
                    try:
                        content = f_handle.read()
                    except:
                        continue
                    res = regex.findall(content)
                    if res:
                        searchResults.append(SearchResult(f, res))
        return searchResults
