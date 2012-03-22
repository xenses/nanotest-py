// nanotest.js
// v1.1.3 - 07 August 2011
//
// A tiny unittest library

//-----------------------------------------------------------------------

// Copyright (c) 2011, Shawn Boyette, Firepear Informatics
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions
// are met:
//
// * Redistributions of source code must retain the above copyright
//   notice, this list of conditions and the following disclaimer.
//
// * Redistributions in binary form must reproduce the above copyright
//   notice, this list of conditions and the following disclaimer in
//   the documentation and/or other materials provided with the
//   distribution.
//
// * Neither the name of Firepear Informatics nor the names of its
//   contributors may be used to endorse or promote products derived
//   from this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
// FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
// COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
// INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
// SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
// HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
// STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
// OF THE POSSIBILITY OF SUCH DAMAGE

//-----------------------------------------------------------------------
// initialization

var jsltest_run  = 0;
var jsltest_pass = 0;

// remap print() if we're inside an HTML document
try {
    if (document) {
        print = function(msg) { var t = document.getElementById('nanotestoutput');
                                t.innerHTML = t.innerHTML + msg + "\n"; };
    }
} catch(err) {
    true;
}

//-----------------------------------------------------------------------
// defuns

function is(expr, expected, msg) {
    if (is_core(expr, expected)) jsltest_pass++;
    else testPrintFailMsg(msg, expected, expr);
}

function isnt(expr, expected, msg) {
    if (!is_core(expr, expected)) jsltest_pass++;
    else testPrintFailMsg(msg, expected, expr, true);
}

function is_core(expr, expected) {
    jsltest_run++;
    if (expr == expected) return true;
    return false;
}

function testPrintFailMsg(msg, expected, result, invert) {
    print("Test " + jsltest_run + " FAILED: " + msg);
    if (invert) {
        print("  Expected anything but " + expected + " and got it anyway");
    } else {
        print("  Expected: '" + expected + "'");
        print("  Got     : '" + result + "'");
    }
}

function testPrintSummary() {
    print("End of test");
    print("  Tests run..... " + jsltest_run);
    print("  Tests passed.. " + jsltest_pass);
    if (jsltest_run == jsltest_pass) {
        print ("Success.");
    } else {
        print(">>>FAIL<<<");
    }
}
