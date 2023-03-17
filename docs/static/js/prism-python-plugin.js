Prism.hooks.add('before-highlightall', function (env) {
    // This plugin improves prism highliting by adding rules that are missing from default
    // prism implementation

    Prism.languages.python = Prism.languages.insertBefore("python", "comment", {
        definition: {
            // Modified behavior of highlighting assignments from the ABNF language
            pattern: /([(, \t]+)(?:[a-z][\w-]*|<[^<>\r\n]*>)(?=\s*=)/m,
            //                 here changed "*" to "+" to filter out assignments from arguments
            //           here added "(," to the group to highlight inline named arguments
            lookbehind: true,
            alias: 'property',
            inside: {
                'punctuation': /<|>/
            }
        },

        libraries: {
            pattern: /\b(?:os|time|numpy|Path)\b/,
            // keywords commonly hightlighted in python editors that are missing from prism
            alias: "keyword"
        },

        GDKeywords: {
            pattern: /\b(sdk|GoodDataSDK|GoodDataSdk)\.\b/,
            // keywords commonly hightlighted in python editors that are missing from prism
            alias: "keyword",
            inside: {
                'punctuation': /\./
                // Avoid higlighting the trailing dot
            }
        }
    }
    )

    function replace(pattern, replacements) {
		return pattern.replace(/<<(\d+)>>/g, function (m, index) {
			return '(?:' + replacements[+index] + ')';
		});
	}
	/**
	 * @param {string} pattern
	 * @param {string[]} replacements
	 * @param {string} [flags]
	 * @returns {RegExp}
	 */
	function re(pattern, replacements, flags) {
		return RegExp(replace(pattern, replacements), flags || '');
	}

	Prism.languages.insertBefore('jsx', 'script', {
		'customScript': {
			// Allow for two levels of nesting
			pattern: re(/=<BRACES>/.source),
			alias: 'language-javascript',
			inside: {
				'script-punctuation': {
					pattern: /^=(?=\{)/,
					alias: 'punctuation'
				},
				rest: Prism.languages.jsx
			},
		}
	}, Prism.languages.jsx.tag);
})