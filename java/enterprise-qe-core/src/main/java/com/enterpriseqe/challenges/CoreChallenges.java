package com.enterpriseqe.challenges;

import java.util.*;

public final class CoreChallenges {
    private CoreChallenges() {}

    public static List<Integer> duplicatesInFirstAppearanceOrder(List<Integer> input) {
        if (input == null || input.isEmpty()) return new ArrayList<>();
        Map<Integer, Integer> counts = new LinkedHashMap<>();
        for (Integer value : input) counts.put(value, counts.getOrDefault(value, 0) + 1);
        List<Integer> out = new ArrayList<>();
        for (Map.Entry<Integer, Integer> e : counts.entrySet()) if (e.getValue() > 1) out.add(e.getKey());
        return out;
    }

    public static Character firstUniqueCharacter(String input) {
        if (input == null || input.isEmpty()) return null;
        Map<Character, Integer> counts = new LinkedHashMap<>();
        for (char c : input.toCharArray()) counts.put(c, counts.getOrDefault(c, 0) + 1);
        for (Map.Entry<Character, Integer> e : counts.entrySet()) if (e.getValue() == 1) return e.getKey();
        return null;
    }

    public static String maskAllButLastFourDigits(String input) {
        if (input == null || input.length() <= 4) return input;
        int totalDigits = 0;
        for (char c : input.toCharArray()) if (Character.isDigit(c)) totalDigits++;
        if (totalDigits <= 4) return input;
        int digitsToMask = totalDigits - 4, seenDigits = 0;
        StringBuilder sb = new StringBuilder(input.length());
        for (char c : input.toCharArray()) {
            if (Character.isDigit(c)) {
                seenDigits++;
                sb.append(seenDigits <= digitsToMask ? '*' : c);
            } else {
                sb.append(c);
            }
        }
        return sb.toString();
    }
}
