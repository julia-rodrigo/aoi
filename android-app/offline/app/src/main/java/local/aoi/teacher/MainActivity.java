package local.aoi.teacher;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;

/**
 * Runs the Aoi Teacher web app bundled inside the APK (assets/www), so it works offline and always
 * matches the build, instead of loading the hosted site. The files are served on a private https
 * origin rather than file:// so the page behaves as it does on the web (storage, audio, fetch to
 * the chat provider).
 */
public class MainActivity extends Activity {
    private static final String HOST = "appassets.androidplatform.net";
    private static final int PICK_FILE = 7;

    private WebView web;
    private ValueCallback<Uri[]> fileCallback;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        web = new WebView(this);
        web.setBackgroundColor(0xFF071034);
        setContentView(web);

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        // Her greeting and lesson voice start without a tap, as they do on the web.
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setAllowFileAccess(false);
        s.setAllowContentAccess(false);

        web.setWebViewClient(new WebViewClient() {
            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest req) {
                Uri u = req.getUrl();
                if (!HOST.equals(u.getHost())) return null;
                String path = u.getPath();
                if (path == null || path.isEmpty() || path.equals("/")) path = "/index.html";
                try {
                    InputStream in = getAssets().open("www" + path);
                    String mime = mimeFor(path);
                    boolean text = mime.startsWith("text/") || mime.endsWith("json") || mime.endsWith("javascript");
                    return new WebResourceResponse(mime, text ? "utf-8" : null, in);
                } catch (IOException e) {
                    return new WebResourceResponse("text/plain", "utf-8", 404, "Not Found",
                            new HashMap<>(), new ByteArrayInputStream(new byte[0]));
                }
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest req) {
                Uri u = req.getUrl();
                if (HOST.equals(u.getHost())) return false;
                // Video searches, docs links and the like open in the phone's browser.
                try {
                    startActivity(new Intent(Intent.ACTION_VIEW, u));
                } catch (ActivityNotFoundException ignored) { }
                return true;
            }
        });

        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> callback, FileChooserParams params) {
                if (fileCallback != null) fileCallback.onReceiveValue(null);
                fileCallback = callback;
                try {
                    startActivityForResult(params.createIntent(), PICK_FILE);
                } catch (ActivityNotFoundException e) {
                    fileCallback = null;
                    return false;
                }
                return true;
            }
        });

        if (savedInstanceState != null) web.restoreState(savedInstanceState);
        else web.loadUrl("https://" + HOST + "/index.html");
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == PICK_FILE && fileCallback != null) {
            fileCallback.onReceiveValue(WebChromeClient.FileChooserParams.parseResult(resultCode, data));
            fileCallback = null;
            return;
        }
        super.onActivityResult(requestCode, resultCode, data);
    }

    /** The phone's back button closes an open panel, then uses the app's own back arrow, then exits. */
    private static final String BACK_JS =
            "(function(){" +
            "var p=document.querySelector('.overlayPanel.open');" +
            "if(p){var c=p.querySelector('.panelHeadBtns button:last-child');if(c){c.click();return 'ok';}}" +
            "var b=document.getElementById('btnBack');" +
            "if(b&&!b.hidden){b.click();return 'ok';}" +
            "return 'exit';})()";

    @Override
    @SuppressWarnings("deprecation")
    public void onBackPressed() {
        web.evaluateJavascript(BACK_JS, value -> {
            if ("\"exit\"".equals(value)) finish();
        });
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        web.saveState(outState);
    }

    @Override
    protected void onPause() {
        super.onPause();
        web.onPause();
    }

    @Override
    protected void onResume() {
        super.onResume();
        web.onResume();
    }

    private static String mimeFor(String path) {
        String p = path.toLowerCase();
        if (p.endsWith(".html")) return "text/html";
        if (p.endsWith(".js")) return "application/javascript";
        if (p.endsWith(".css")) return "text/css";
        if (p.endsWith(".json") || p.endsWith(".webmanifest")) return "application/json";
        if (p.endsWith(".png")) return "image/png";
        if (p.endsWith(".svg")) return "image/svg+xml";
        if (p.endsWith(".jpg") || p.endsWith(".jpeg")) return "image/jpeg";
        if (p.endsWith(".mp3")) return "audio/mpeg";
        if (p.endsWith(".wav")) return "audio/wav";
        if (p.endsWith(".woff2")) return "font/woff2";
        return "application/octet-stream";
    }
}
