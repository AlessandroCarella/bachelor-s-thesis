def reorderEntries(entries: list, maxNumberOfCharsForFrames:int, maxNumberOfCharsForUseOfFrame:int) -> list:
    def sortKey(line):
        frameAndUseOfFrame = line.split(",")[0].replace("entry(", "")
        frame = int(frameAndUseOfFrame[:maxNumberOfCharsForFrames])
        useOfFrame = int(frameAndUseOfFrame[:maxNumberOfCharsForUseOfFrame])
        return (frame, useOfFrame)

    return sorted(entries, key=sortKey)
    