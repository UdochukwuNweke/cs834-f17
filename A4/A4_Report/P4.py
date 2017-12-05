 

 private String generateSnippet(
          final Document document,
          final ArrayList<IntSpan> positions,
          final Set<String> queryTerms) {
    ArrayList<SnippetRegion> regions = findMatches(document, queryTerms);
    ArrayList<SnippetRegion> finalRegions = combineRegions(regions);
    Snippet best = new Snippet(finalRegions);

    return buildHtmlString(best, document, positions);
  }