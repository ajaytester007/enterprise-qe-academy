package com.enterpriseqe.academy;

import org.junit.jupiter.api.Test;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

class CoreChallengesTest {
    @Test
    void duplicateValuesPreserveFirstAppearanceOrder() {
        assertEquals(List.of(1, 2), CoreChallenges.duplicatesInFirstAppearanceOrder(List.of(1,2,3,2,4,5,1)));
        assertEquals(List.of(1), CoreChallenges.duplicatesInFirstAppearanceOrder(List.of(1,3,1,5)));
    }

    @Test
    void firstUniqueCharacterIsDeterministic() {
        assertEquals('u', CoreChallenges.firstUniqueCharacter("automation"));
        assertNull(CoreChallenges.firstUniqueCharacter("mama"));
        assertEquals('b', CoreChallenges.firstUniqueCharacter("abac"));
        assertEquals('c', CoreChallenges.firstUniqueCharacter("aabbc"));
    }

    @Test
    void masksSensitiveDataPreservingSeparators() {
        assertEquals("*****6789", CoreChallenges.maskAllButLastFourDigits("123456789"));
        assertEquals("1234", CoreChallenges.maskAllButLastFourDigits("1234"));
        assertEquals("***-**-6789", CoreChallenges.maskAllButLastFourDigits("123-45-6789"));
    }
}
